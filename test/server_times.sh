apps=("gabrielvoicu200-worker-asia-0" "gabrielvoicu200-worker-asia-1" "gabrielvoicu200-worker-emea-0" "gabrielvoicu200-worker-us-0" "gabrielvoicu200-worker-us-1")

echo "Getting all service times from servers"
for app in "${apps[@]}"; do
  heroku logs -a "$app" -n 1500 | awk '/service/ {print $11}' | cut -d '=' -f 2 | sed 's/..$//' | head -c -1 | tr '\n' ' ' > times_"$app".txt
done