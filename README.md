

## Generate the sqlmodel schema

```shell
$ pip install "sqlacodegen @git+https://github.com/agronholm/sqlacodegen.git"
$ sqlacodegen --generator sqlmodels --noviews --outfile model.py sqlite:///./memego.db 


$ sqlacodegen --generator declarative --noviews --outfile model.py sqlite:///./memego.db 
```