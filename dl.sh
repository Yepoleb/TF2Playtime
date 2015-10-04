GROUPNAME="tf2-highlander"
PAGES=33

for ((i=1; i<= $PAGES; i++));
do
  curl "http://steamcommunity.com/groups/${GROUPNAME}/members/?p=${i}&content_only=true" -o "group/${GROUPNAME}_${i}.html"
done
