import json
from pathlib import Path
import sys
import tempfile
from repror import conf
from repror.build import Recipe


if __name__ == "__main__":
    # Prepare the matrix
    only_one = True if len(sys.argv) == 2 and sys.argv[1] == "onle_one" else False
    recipe_list = []

    config = conf.load_config()

    with tempfile.TemporaryDirectory() as tmp_dir:
        for repo in config.get("repositories", []):
            url = repo["url"]
            branch = repo["branch"]
            for recipe in repo.get("recipes", []):
                path = recipe["path"]

                recipe = Recipe(
                    url=url, branch=branch, recipe_path=path, recipe_type="remote"
                )
                recipe_config = conf.RecipeConfig.load_remote_recipe(
                    recipe, Path(tmp_dir)
                )
                recipe.name = recipe_config.name

                recipe_list.append(recipe.__dict__)

        for local in config.get("local", []):
            path = local["path"]
            recipe = Recipe(
                url=None, branch=None, recipe_path=path, recipe_type="local"
            )
            recipe_config = conf.RecipeConfig.load_local_recipe(recipe.recipe_path)
            recipe.name = recipe_config.name

            recipe_list.append(recipe.__dict__)

    if only_one:
        print(json.dumps(recipe_list[0]))
    else:
        print(json.dumps(recipe_list))
