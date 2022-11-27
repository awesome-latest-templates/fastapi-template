

## Generate the sqlmodel schema

```shell
$ pip install "sqlacodegen @git+https://github.com/agronholm/sqlacodegen.git"
$ sqlacodegen --generator sqlmodels --noviews --outfile model.py sqlite:///./memego.db 


$ sqlacodegen --generator declarative --noviews --outfile model.py sqlite:///./memego.db 
```


## References

- [fastapi-alembic-sqlmodel-async](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async/tree/main/fastapi-alembic-sqlmodel-async/app/api)
- [fastapi-role-based-access-control-auth-service](https://github.com/tsatsujnr139/fastapi-role-based-access-control-auth-service/blob/master/app/crud/base.py)
- [fastapi-mvc-loguru-demo](https://github.com/abnerjacobsen/fastapi-mvc-loguru-demo/blob/main/mvc_demo/wsgi.py)
