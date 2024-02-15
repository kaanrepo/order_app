data "external_schema" "django" {
  program = [
    "python",
    "manage.py",
    "atlas-provider-django",
    "--dialect", "mysql" // mariadb | postgresql | sqlite | mssql
    
    // if you want to only load a subset of your app models, you can specify the apps by adding
    // "--apps", "app1", "app2", "app3"
  ]
}

env "django" {
  src = data.external_schema.django.url
  dev = "docker://mysql/8/dev"
  migration {
    dir = "file://migrations"
  }
  format {
    migrate {
      diff = "{{ sql . \"  \" }}"
    }
  }
}