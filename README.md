# informant

A graphical view into your CloudTrail records

## How To

### With a container

```bash
docker run -dit -p <desiredPort>:80 --name informant <image_location>
```

Possible arguments:

* --env-file <location> # Required for environment variables for SDK keys if instance profile isn't used
* -v <location>:/var/www/html/searches # Required if you want the search data to be stored on the host rather than within the container
