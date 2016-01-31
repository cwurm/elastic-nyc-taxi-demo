from elasticsearch import Elasticsearch
import pdb

indexName = "nyc_taxi-predict"
docType = "rides"

indexSettings = {
	"mappings": {
	   docType: {
		   "properties": {
			   "pickup_datetime": {
				   "type": "date"
			   },
			   "count": {
				   "type": "float"
			   }
		   }
	   }
	}
}

es = Elasticsearch()

# Delete and recreate index
if es.indices.exists(indexName):
    es.indices.delete(index = indexName)
es.indices.create(index = indexName, body = indexSettings)

query = {
	"aggs": {
		"my_date_histo":{                
			"date_histogram":{
				"field":"pickup_datetime",
				"interval":"hour"
			},
			"aggs":{
				"the_count":{
					"value_count":{ "field": "fare_amount" } 
				},
				"the_movavg":{
					"moving_avg":{
					  "buckets_path": "the_count",
					  "model": "holt_winters",
					  "window": 168,
					  "predict": 72,
					  "settings": {
						  "period": 24
					  }
					}
				}
			}
		}
	},
	"size": 0
}

result = es.search(index = "nyc_taxi-2014-11", body = query)

for bucket in result["aggregations"]["my_date_histo"]["buckets"]:
	date = bucket["key"]
	val = None

	if "the_movavg" in bucket:
		val = bucket["the_movavg"]["value"]

	doc = {
		"pickup_datetime": date,
		"count": val
	}

	es.index(index = indexName, doc_type = docType, body = doc)

