from flask import jsonify, request
from flask_restful import Resource

from . import models


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


class AnalyzeResource(Resource):
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
