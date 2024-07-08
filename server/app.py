# from models import db, User, Event, Ticket, Payment, EventBookmark
from models import db, EventBookmark, Payment, Ticket, Event, User
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
from auth import jwt, auth_bp, bcrypt
from flask_jwt_extended import jwt_required, current_user

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

app.config['SECRET_KEY'] = 'bfd44160eee50045cba10da003f8267b'

app.register_blueprint(auth_bp)
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)
api=Api(app)



@app.route('/')
def index():
    return f'Welcome to phase 4 Project'


class ShowUsers(Resource):
    @jwt_required()
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)
    

    def post(self):
        data = request.get_json()

        if not data or not data.get('username') or not data.get('email'):
            return {"message": "Required (username and email)"}, 400

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return {"message": "User with this email already exists"}, 400
        
        new_user = User(username=data['username'], email=data['email'])
        try:
            db.session.add(new_user)
            db.session.commit()
            user_dict = new_user.to_dict()
            response = make_response(user_dict, 201)
            return response
        
        except Exception as exc:
            db.session.rollback()
            return {"message": "Error creating user", "error": str(exc)}, 500

api.add_resource(ShowUsers, '/users')


class ShowUser(Resource):
    def get(self, id):
        user = User.query.filter(User.id == id).first()
        if not user:
            return {"message": "User not found"}, 404
        return user.to_dict(), 200

    def patch(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"message": "User not found"}, 404
        
        data = request.get_json()
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        try:
            db.session.commit()
            return user.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating user", "error": str(e)}, 500

    def delete(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {"message": "User not found"}, 404
        try:
            db.session.delete(user)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting user", "error": str(e)}, 500

api.add_resource(ShowUser, '/users/<int:id>')




class ShowEventBookmarks(Resource):
    def get(self):
        eventbookmarks = [eventbookmark.to_dict() for eventbookmark in EventBookmark.query.all()]
        return make_response(eventbookmarks, 200)
    

    def post(self):
        data = request.get_json()
        if not data or not data.get('user_id') or not data.get('event_id'):
            return {"message": "Required (user_id and event_id)"}, 400

        user = User.query.get(data['user_id'])
        if not user:
            return {"message": "User not found"}, 404

        event = Event.query.get(data['event_id'])
        if not event:
            return {"message": "Event not found"}, 404

        new_eventbookmark = EventBookmark(user_id=data['user_id'], event_id=data['event_id'])
        try:
            db.session.add(new_eventbookmark)
            db.session.commit()
            return {"message": "EventBookmark created Successfully", "eventbookmark": new_eventbookmark.to_dict()}, 201
        except Exception as exc:
            db.session.rollback()
            return {"message": "Error creating event bookmark", "error": str(exc)}, 500    
    
api.add_resource(ShowEventBookmarks, '/eventbookmarks')



class ShowEventBookmark(Resource):
    def get(self, id):
        eventbookmark = EventBookmark.query.filter(User.id==id).first()
        if not eventbookmark:
            return {"message": "EventBookmark not found"}, 404
        return eventbookmark.to_dict(), 200
    

    def patch(self, id):
        data = request.get_json()

        eventbookmark = EventBookmark.query.filter(User.id==id).first()
        if not eventbookmark:
            return {"message": "Event bookmark not found"}, 404

        if 'user_id' in data:
            eventbookmark.user_id = data['user_id']
        if 'event_id' in data:
            eventbookmark.event_id = data['event_id']
        
        try:
            db.session.commit()
            return eventbookmark.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating event bookmark", "error": str(e)}, 500
    

    def delete(self, id):
        eventbookmark = EventBookmark.query.filter_by(id=id).first()
        if not eventbookmark:
            return {"message": "Event bookmark not found"}, 404
        
        try:
            db.session.delete(eventbookmark)
            db.session.commit()
            return {}, 204
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting event bookmark", "error": str(e)}, 500

api.add_resource(ShowEventBookmark, '/eventbookmarks/<int:id>')



class ShowPayments(Resource):
    def get(self):
        payments = [payment.to_dict() for payment in Payment.query.all()]
        return make_response(payments, 200)

    def post(self):
        data = request.get_json()
        if not data or not data.get('amount') or not data.get('status') or not data.get('user_id'):
            return {"message": "Missing required fields (amount, status, user_id)"}, 400

        user = User.query.get(data['user_id'])
        if not user:
            return {"message": "User not found"}, 404

        event_id = data.get('event_id')
        if event_id:
            event = Event.query.get(event_id)
            if not event:
                return {"message": "Event not found"}, 404

        ticket_id = data.get('ticket_id')
        if ticket_id:
            ticket = Ticket.query.get(ticket_id)
            if not ticket:
                return {"message": "Ticket not found"}, 404

        new_payment = Payment(
            amount=data['amount'],
            status=data['status'],
            user_id=data['user_id'],
            event_id=event_id,
            ticket_id=ticket_id
        )

        try:
            db.session.add(new_payment)
            db.session.commit()
            return {"message": "Payment created successfully", "payment": {
                "id": new_payment.id,
                "amount": new_payment.amount,
                "status": new_payment.status,
                "created_at": new_payment.created_at.isoformat(),
                "updated_at": new_payment.updated_at.isoformat() if new_payment.updated_at else None,
                "user_id": new_payment.user_id,
                "event_id": new_payment.event_id,
                "ticket_id": new_payment.ticket_id
            }}, 201
        except Exception as e:
            db.session.rollback()
            return {"message": "Error creating payment", "error": str(e)}, 500

api.add_resource(ShowPayments, '/payments')


class ShowPayment(Resource):
    def get(self, id):
        payment = Payment.query.filter(Payment.id==id).first()
        if not payment:
            return {"message": "Payment not found"}, 404
        return payment.to_dict(), 200


    def patch(self, id):
        payment = Payment.query.get(id)
        if not payment:
            return {"message": "Payment not found"}, 404

        data = request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400

        # Update payment fields
        if 'amount' in data:
            payment.amount = data['amount']
        if 'status' in data:
            payment.status = data['status']
        if 'user_id' in data:
            payment.user_id = data['user_id']
        if 'event_id' in data:
            payment.event_id = data['event_id']
        if 'ticket_id' in data:
            payment.ticket_id = data['ticket_id']

        try:
            db.session.commit()
            return {"message": "Payment updated successfully", "payment": {
                "id": payment.id,
                "amount": payment.amount,
                "status": payment.status,
                "created_at": payment.created_at.isoformat(),
                "updated_at": payment.updated_at.isoformat() if payment.updated_at else None,
                "user_id": payment.user_id,
                "event_id": payment.event_id,
                "ticket_id": payment.ticket_id
            }}
        except Exception as e:
            db.session.rollback()
            return {"message": "Error updating payment", "error": str(e)}, 500


    def delete(self, id):
        payment = Payment.query.filter_by(id=id).first()
        if not payment:
            return {"message": "Payment not found"}, 404

        try:
            db.session.delete(payment)
            db.session.commit()
            return {}, 204
        
        except Exception as e:
            db.session.rollback()
            return {"message": "Error deleting payment", "error": str(e)}, 500

api.add_resource(ShowPayment, '/payments/<int:id>')


class ShowTickets(Resource):
    def get(self):
        tickets = [ticket.to_dict() for ticket in Ticket.query.all()]
        return make_response(tickets, 200)
    
api.add_resource(ShowTickets, '/tickets')



class ShowEvents(Resource):
    def get(self):
        events = [event.to_dict() for event in Event.query.all()]
        return make_response(events, 200)
    
api.add_resource(ShowEvents, '/events')



if __name__ == '__main__':
    app.run(port='5555', debug=True)