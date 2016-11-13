from flask import jsonify, request
from flask_restful import Resource, reqparse
from datetime import datetime

from HarassBlockNLP import HarassBlock

from . import models, db


class SiteResource(Resource):
    def get(self, id):
        site = models.Site.query.get(id)
        if site:
            result = {
                'url': site.url,
                'rating': site.average_rating,
                'votes': site.number_of_votes
            }
            return jsonify(result)
        else:
            return jsonify(result='Not Found')


class VoteResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('url')
        self.parser.add_argument('rating')

    def get(self):
        args = self.parser.parse_args()
        if 'url' not in args or 'rating' not in args:
            return jsonify(error='URL not passed in')

        site = models.Site.query.filter(models.Site.url == args['url']).first()
        site.votes.append(models.Vote(rating=args['rating'], time=datetime.now()))
        db.session.commit()
        return jsonify(result='success')


class AnalyzeResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('url')

    def get(self):
        args = self.parser.parse_args()
        if 'url' not in args:
            return jsonify(error='URL not passed in')

        site = models.Site.query.filter(models.Site.url == args['url']).first()
        if not site:
            site = models.Site(url=args['url'])
            db.session.add(site)

        # past_analysis = models.Analysis.query.filter(
        #     models.Analysis.site_id == site.id
        #     ).order_by(models.Analysis.time.desc()).first()
        # if past_analysis:
        #     latest_analysis = past_analysis
        # else:
        negativity = HarassBlock().analyze(args['url'])
        latest_analysis = models.Analysis(negativity=negativity, time=datetime.now())
        site.analyses.append(latest_analysis)

        result = {
            'url': site.url,
            'rating': site.average_rating,
            'votes': site.number_of_votes,
            'analysis': {
                'negativity': latest_analysis.negativity,
                'time': latest_analysis.time
            }
        }
        db.session.commit()
        return jsonify(result)

    def post(self):
        data = request.get_json(force=True)
        if 'url' not in data:
            return jsonify(error='URL not passed in')
        url = data['url']
        site = models.Site.query.filter(models.Site.url == url).first()
        if site:
            result = {
                'url': site.url,
                'rating': site.average_rating,
                'votes': site.number_of_votes
            }
            return jsonify(result)
        else:
            return jsonify(result='Not Found')
