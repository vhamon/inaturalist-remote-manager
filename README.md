# inaturalist-remote-manager
Simple python client using fast iNaturalist's REST API

## REST API doc
https://api.inaturalist.org/v1/docs/#/

## API token
Authentication in the Node API is handled via JSON Web Tokens (JWT). To obtain one, make an OAuth-authenticated request to https://www.inaturalist.org/users/api_token. Each JWT will expire after 24 hours. Authentication required for all PUT and POST requests. Some GET requests will also include private information like hidden coordinates if the authenticated user has permission to view them.