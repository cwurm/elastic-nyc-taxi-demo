# NYC Taxi demo

## Download CSV
Go to http://www.nyc.gov/html/tlc/html/about/trip_record_data.shtml and download the CSV file for November 2014 (yellow cabs).

## Index
Run (replace `$logstash` with the path to a Logstash 2.x executable):
```
tail -n +2 yellow_tripdata_2014-11.csv | $logstash -f logstash.conf
```

## Predict
Execute `python predict.py`. You will need to modify it to use authentication if your Elasticsearch cluster is thus protected.

## Kibana
1. Create two new index patterns:`nyc_taxi-2014-11` and `nyc_taxi-predict` (no wildcards). Select `pickup_datetime` as the Time-field name for both.
2. Import `kibana-visualizations.json` and `kibana-dashboards.json`, in that order.
