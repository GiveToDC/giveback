# Load cards
Be aware the GiveCard endpoint for loading cards takes a string ("5.55" -> $5.55), not an int or float.

## Cloud Resources
### PubSub
Cloud Build sets the function trigger for us as long as the topic exists.

Uses a JSON encoded topic called `load_cards`, with a schema called `load_cards`:
```JSON
{
  "type": "record",
  "name": "load_cards",
  "fields": [
    {
      "name": "amount",
      "type": "string"
    }
  ]
}
```

### Cloud Scheduler
The function is intended to be fired through the `load_cards` PubSub topic with a Cloud Scheduler job called `load_cards_daily`.

The job has frequency `0 6 * * 1-7`, every morning at 6 AM.

The timezone is set to EDT.

The job targets the `load_cards` PubSub topic with a message body of:
```JSON
{
	"amount":"5"
}
```