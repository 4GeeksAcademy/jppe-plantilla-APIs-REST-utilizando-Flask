from flask_sqlalchemy import SQLAlchemy
import os
import sys

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favoritos_P = db.relationship('Favoritos_P', backref='user', lazy=True)
    favoritos_Planetas = db.relationship('Favoritos_Planetas', backref='user', lazy=True)
   
    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
   
    

class Planetas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    terreno = db.Column(db.String(120), unique=True, nullable=False)
    clima = db.Column(db.String(120), unique=True, nullable=False)
    favoritos_Planetas = db.relationship('Favoritos_Planetas', backref='planetas', lazy=True)

    def __repr__(self):
        return '<Planetas %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terreno": self.terreno,
            "clima": self.clima,
            "favoritos_Planetas": self.favoritos_Planetas
            # do not serialize the password, its a security breach
        }
    
class Personajes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    nacimiento = db.Column(db.String(120), unique=True, nullable=False)
    especie = db.Column(db.String(120), unique=True, nullable=False)
    altura = db.Column(db.String(120), unique=True, nullable=False)
    peso = db.Column(db.String(120), unique=True, nullable=False)
    genero = db.Column(db.String(120), unique=True, nullable=False)
    color_pelo = db.Column(db.String(120), unique=True, nullable=False)
    favoritos_P = db.relationship('Favoritos_P', backref='personajes', lazy=True)
   

    def __repr__(self):
        return '<Personajes %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "nacimiento": self.nacimiento,
            "especie": self.especie,
            "altura": self.altura,
            "peso": self.peso,
            "genero": self.genero,
            "color_pelo": self.color_pelo,
            "favoritos_P": self.favoritos_P
            # do not serialize the password, its a security breach
        }
    
class Vehiculos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    Model = db.Column(db.String(120), unique=True, nullable=False)
    Manufacturer = db.Column(db.String(120), unique=True, nullable=False)
    Class = db.Column(db.String(120), unique=True, nullable=False)
    Cargo_Capacity = db.Column(db.String(120), unique=True, nullable=False)
    Length = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Vehiculos %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "Model": self.Model,
            "Manufacturer": self.Manufacturer,
            "Class": self.Class,
            "Cargo_Capacity": self.Cargo_Capacity,
            "Length": self.Length,
            # do not serialize the password, its a security breach
        }
    
     
        
class Favoritos_P(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    personajes_id = db.Column(db.Integer, db.ForeignKey('personajes.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Favoritos_P %r>' % self.id

    def serialize(self):
        return {
            "personajes_id": self.personajes_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }

class Favoritos_Planetas(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    planetas_id = db.Column(db.Integer, db.ForeignKey('planetas.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


    def __repr__(self):
        return '<Favoritos_Planetas %r>' % self.id

    def serialize(self):
        return {
            "planetas_id": self.planetas_id,
            "user_id": self.user_id,
            # do not serialize the password, its a security breach
        }