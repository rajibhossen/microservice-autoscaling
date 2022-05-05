kubectl exec -n media-microsvc review-storage-mongodb-9c886d5d7-nlbmk -- mongo review --eval "db.review.remove({})"
kubectl exec -n media-microsvc movie-review-mongodb-5645d78c84-5v7xp -- mongo movie-review --eval "db['movie-review'].remove({})"
kubectl exec -n media-microsvc user-review-mongodb-8d9995d87-fqmfk -- mongo user-review --eval "db['user-review'].remove({})"