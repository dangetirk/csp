select id from {{source('curated','rskcsp_ds_cardholder_curated')}}
where length(id) > 18