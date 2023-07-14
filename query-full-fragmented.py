def get_query(start_index, end_index):
  pipeline = [
   {
      "$match":{
         "tracks.items":{
            "$ne":[
               
            ],
            "$exists":true
         }
      }
   },
   {
      "$unwind":"$tracks.items"
   },
   {
      "$group":{
         "_id":"$tracks.items.external_ids.isrc",
         "popularity":{
            "$first":"$tracks.items.popularity"
         },
         "track_name":{
            "$first":"$tracks.items.name"
         },
         "artist_name":{
            "$first":"$tracks.items.artists.name"
         },
         "artist_id":{
            "$first":"$tracks.items.artists.id"
         },
         "genre":{
            "$addToSet":"$genre_track"
         }
      }
   },
   {
      "$project":{
         "_id":0,
         "isrc":"$_id",
         "popularity":1,
         "track_name":1,
         "genre":1,
         "artist_id":{
            "$arrayElemAt":[
               "$artist_id",
               0
            ]
         },
         "artist_name":{
            "$arrayElemAt":[
               "$artist_name",
               0
            ]
         }
      }
   },
   {
      "$sort":{
         "popularity":-1
      }
   },
   {
      "$skip": start_index
   },
   {
      "$limit": end_index - start_index
   }
]

return pipeline
