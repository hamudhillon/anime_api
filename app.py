from flask import Flask
from flask_restful import Api,Resource,reqparse,abort,fields,marshal_with
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
import requests

# import re
# from urllib.request import urlopen,Request
# import os
# import json
from bs4 import BeautifulSoup

app=Flask(__name__)
api=Api(app)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///animedatabase.db'
db=SQLAlchemy(app)

class Animemodel(db.Model):
    id=db.Column(db.Text,primary_key=True)
    Title=db.Column(db.Text,nullable=False)
    ani_thumb=db.Column(db.Text,nullable=False)
    ani_desc=db.Column(db.Text,nullable=False)
    ani_episodes=db.Column(db.Text,nullable=False)
    
    def __repr__(self):
        return f"Anime(Title={Title},ani_thumb={ani_thumb},ani_desc={ani_desc}),ani_episodes={ani_episodes}"
    
class AnimeEpmodel(db.Model):
    id=db.Column(db.Text,primary_key=True)
    animeid=db.Column(db.Text,nullable=False)
    epi_num=db.Column(db.Text,nullable=False)
    epi_time=db.Column(db.Text,nullable=False)
    epi_type=db.Column(db.Text,nullable=False)
    media=db.Column(db.Text,nullable=False)
    
    def __repr__(self):
        return f"Anime(animeid={animeid},epi_num={epi_num},epi_time={epi_time},epi_type={epi_type}),media={media}"
    
anime_put_args=reqparse.RequestParser()
anime_put_args.add_argument('Title',type=str,help="Title of User is required",required=True)
anime_put_args.add_argument('ani_thumb',type=str,help="ani_thumb of User is required",required=True)
anime_put_args.add_argument('ani_desc',type=str,help="ani_desc of User is required",required=True)
anime_put_args.add_argument('ani_episodes',type=str,help="ani_episodes of User is required",required=True)

animeEp_put_args=reqparse.RequestParser()
animeEp_put_args.add_argument('animeid',type=str,help="Title of User is required",required=True)
animeEp_put_args.add_argument('epi_num',type=str,help="Title of User is required",required=True)
animeEp_put_args.add_argument('epi_time',type=str,help="ani_thumb of User is required",required=True)
animeEp_put_args.add_argument('epi_type',type=str,help="ani_desc of User is required",required=True)
animeEp_put_args.add_argument('media',type=str,help="ani_episodes of User is required",required=True)


# db.create_all()
resource_fields={
    'id':fields.String,
    'Title':fields.String,
    'ani_thumb':fields.String,
    'ani_desc':fields.String,
    'ani_episodes':fields.String,
}
epresource_fields={
    'id':fields.String,
    'animeid':fields.String,
    'epi_num':fields.String,
    'epi_time':fields.String,
    'epi_type':fields.String,
    'media':fields.String,
}


class Anime(Resource):
    @marshal_with(resource_fields)
    def get(self,ani_Title):
        result=Animemodel.query.filter_by(Title=ani_Title).first()
        if not result:
            abort(404,message='Anime Not Found')
        return result
class Anime_all(Resource):
    @marshal_with(resource_fields)
    def get(self):
        result=Animemodel.query.all()
        if not result:
            abort(404,message='Anime Not Found')
        return result
class Addanime(Resource):
    @marshal_with(resource_fields)
    def put(self,uid):
        args=anime_put_args.parse_args()
        result=Animemodel.query.filter_by(id=uid).first()
        if result:
            abort(409,message="Anime is already there id taken..")
        user=Animemodel(id=uid,Title=args['Title'],ani_thumb=args['ani_thumb'],ani_desc=args['ani_desc'],ani_episodes=args['ani_episodes'])
        db.session.add(user)
        db.session.commit()
        
        return user,201
class anime_episodes(Resource):
    @marshal_with(epresource_fields)
    def get(self,uid):
        result=AnimeEpmodel.query.filter_by(animeid=uid).all()
        if not result:
            abort(404,message='Anime Not Found')
        return result
class Addanime_episodes(Resource):
    @marshal_with(resource_fields)
    def put(self,uid):
        args=animeEp_put_args.parse_args()
        result=AnimeEpmodel.query.filter_by(id=uid).first()
        if result:
            abort(409,message="Anime Episode is already there id taken..")
        user=AnimeEpmodel(id=uid,animeid=args['animeid'],epi_num=args['epi_num'],epi_time=args['epi_time'],epi_type=args['epi_type'],media=args['media'])
        db.session.add(user)
        db.session.commit()
        
        return user,201

api.add_resource(Addanime,'/anime/<uid>')
api.add_resource(Addanime_episodes,'/anime-episodes/<uid>')
api.add_resource(anime_episodes,'/anime-episodes/<uid>')
api.add_resource(Anime,'/anime/<ani_Title>')
api.add_resource(Anime_all,'/anime/all')
# api.add_resource(Image,'/')

if __name__ =="__main__":
    app.run(debug=True)