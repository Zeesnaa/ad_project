# Asset Dash project

## Instructions
### Quickstart 
```bash
git clone https://github.com/Zeesnaa/ad_project.git .
docker build -t ad_project .
docker run -p 5050:5050 ad_project
```
### Testing first question
* `curl "localhost:5050/portfolio-chart?user_id=user_1"`
* `curl "localhost:5050/portfolio-chart?user_id=user_123"` (user not found)
* `curl "localhost:5050/portfolio-chart?user_id="` (user null)

### Testing second question
* `curl "localhost:5050/portfolio-holdings?user_id=user_1"` 
* `curl "localhost:5050/portfolio-holdings?user_id="`(user null)
* `curl "localhost:5050/portfolio-holdings?user_id=123"` (user not found)
* `curl "localhost:5050/portfolio-holdings?user_id=user_1&asset_type=crypto"` (filtering active)
* `curl "localhost:5050/portfolio-holdings?user_id=user_1&asset_type=stonks"` (invalid asset filter)
