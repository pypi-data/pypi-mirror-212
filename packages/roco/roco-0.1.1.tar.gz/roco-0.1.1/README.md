# Roco - Runtime config generator

Command line utility tool which prints to the standard output javascript valid 
text generated from environment variables.

For example, given following environment variables:

    PAPERMERGE__AUTH__GOOGLE_CLIENT_ID=some-id.apps.googleusercontent.com
    PAPERMERGE__AUTH__GOOGLE_AUTHORIZE_URL=https://accounts.google.com/o/oauth2/auth
    PAPERMERGE__AUTH__GOOGLE_REDIRECT_URI=http://localhost:11000/google/callback

will result in the following text (valid javascript) as output:

    window.__PAPERMERGE_RUNTIME_CONFIG__ = {
      oauth2: {
        google: {
          client_id: 'some-id.apps.googleusercontent.com',
          authorize_url: 'https://accounts.google.com/o/oauth2/auth',
          redirect_uri: 'http://localhost:11000/google/callback',
          scope: 'openid email',
        },
      }
    };


## Install

    pip install roco

## Usage

If no relevant environment variables were defined just running:

    roco

Will result in following output:

    window.__PAPERMERGE_RUNTIME_CONFIG__ = {
    };

i.e. valid, but empty, javascript object.
In order to see current roco's pydantic settings (read from env vars)
run:
    
    roco -s

The above command will also show the env var prefix i.e. `PAPERMERGE__AUTH__`.

Roco reads from following environment variables:

* `PAPERMERGE__AUTH__GOOGLE_AUTHORIZE_URL`
* `PAPERMERGE__AUTH__GOOGLE_CLIENT_ID`
* `PAPERMERGE__AUTH__GOOGLE_REDIRECT_URI`
* `PAPERMERGE__AUTH__GITHUB_AUTHORIZE_URL`
* `PAPERMERGE__AUTH__GITHUB_CLIENT_ID`
* `PAPERMERGE__AUTH__GITHUB_REDIRECT_URI`
