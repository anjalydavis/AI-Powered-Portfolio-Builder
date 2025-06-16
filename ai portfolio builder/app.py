from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from ai import call_google_ai_model

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(100), nullable=False)

class UserDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(255), nullable=False)
    program_name_1 = db.Column(db.String(100), nullable=False)
    program_1_university = db.Column(db.String(100), nullable=False)
    program1_year = db.Column(db.String(50), nullable=False)
    program1_skills = db.Column(db.Text, nullable=False)
    program_name_2 = db.Column(db.String(100), nullable=False)
    program_2_university = db.Column(db.String(100), nullable=False)
    program2_year = db.Column(db.String(50), nullable=False)
    program2_skills = db.Column(db.Text, nullable=False)
    project1_name = db.Column(db.String(100), nullable=False)
    project1_description = db.Column(db.Text, nullable=False)
    project1_skills = db.Column(db.Text, nullable=False)
    project2_name = db.Column(db.String(100), nullable=False)
    project2_description = db.Column(db.Text, nullable=False)
    project2_skills = db.Column(db.Text, nullable=False)
    project3_name = db.Column(db.String(100), nullable=False)
    project3_description = db.Column(db.Text, nullable=False)
    project3_skills = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    about_me = db.Column(db.Text, nullable=False)

@app.route('/')
def landing_page():
    return render_template("landing_page.html")

@app.route('/view-portfolio/<int:id>')
def view_portfolio(id):
    user_data = UserDetails.query.get_or_404(id)
    return render_template("portfolio.html", user=user_data)

@app.route('/contact-form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        new_contact = Contact(
            name=request.form['name'],
            email=request.form['email'],
            subject=request.form['subject'],
            message=request.form['message']
        )
        db.session.add(new_contact)
        db.session.commit()
        return "Thank you! We will get back to you soon."
    return redirect(url_for('landing_page'))

@app.route('/list-contacts')
def list_contacts():
    contacts = Contact.query.all()
    return render_template("list-contacts.html", contacts_list=contacts)

@app.route('/create-portfolio', methods=['GET', 'POST'])
def create_portfolio():
    data = {
        'name': '',
        'title': '',
        'profile_picture': '',
        'program_name_1': '',
        'program_1_university': '',
        'program1_year': '',
        'program1_skills': '',
        'program_name_2': '',
        'program_2_university': '',
        'program2_year': '',
        'program2_skills': '',
        'project1_name': '',
        'project1_description': '',
        'project1_skills': '',
        'project2_name': '',
        'project2_description': '',
        'project2_skills': '',
        'project3_name': '',
        'project3_description': '',
        'project3_skills': '',
        'email': '',
        'location': '',
        'phone': '',
        'about_me': ''
    }

    if request.method == 'POST':
        form_data = request.form
        if form_data['about_me'] == "generating...":
            data.update(form_data.to_dict())
            data['about_me'] = call_google_ai_model(data)
            return render_template("form.html", data=data)
        else:
            new_portfolio = UserDetails(**form_data.to_dict())
            db.session.add(new_portfolio)
            db.session.commit()
            return redirect(url_for('view_all_portfolios'))

    return render_template("form.html", data=data)

@app.route('/all-portfolios')
def view_all_portfolios():
    portfolios = UserDetails.query.all()
    return render_template("all-portfolio.html", data=portfolios)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)