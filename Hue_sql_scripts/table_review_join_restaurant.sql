SELECT r.user_id,r_b.name,r_b.business_id,r_b.categories,r.text,r_b.attributes,r_b.latitude,r_b.longitude,r_b.open,r_b.full_address ,r.stars
FROM review r JOIN restaurant r_b
ON (r.business_id = r_b.business_id)
