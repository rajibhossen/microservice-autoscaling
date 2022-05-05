kubectl exec -n sock-shop carts-db-5bdf5d4669-6qg6q -- mongo data --eval "db.cart.remove({})"
kubectl exec -n sock-shop carts-db-5bdf5d4669-6qg6q -- mongo data --eval "db.item.remove({})"
kubectl exec -n sock-shop orders-db-5d465875cc-hkmvd -- mongo data --eval "db.customerOrder.remove({})"
