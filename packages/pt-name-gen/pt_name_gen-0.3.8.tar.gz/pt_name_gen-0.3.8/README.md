# pt_name_gen #

A Python module for generating random names in Portuguese.

### Installation ###

To install the name_generator module, use pip:

```
pip install pt_name_gen
```

### Usage ###

To use pt_name_gen, import the `pt_name_gen` function from the `pt_name_gen` module and call it to generate a random name.

The gender parameter should be 0 for male names or 1 for female names. If no gender parameter is specified, a random gender will be chosen.

You can access these attributes using dot notation, like this:

```
from pt_name_gen import pt_name_gen

person = pt_name_gen.generate_name(0)  # Male
print(person.full_name)  # Prints the full name of the person
print(person.email)      # Prints the email address of the person
```

The `pt_name_gen` function returns a `Person` object, which has the following attributes:

* `first_name`: The first name of the person (e.g. "John").
* `last_name`: The last name of the person (e.g. "Smith").
* `full_name`: The full name of the person (e.g. "John Smith").
* `email`: The email address of the person (e.g. "johnsmith@gmail.com").
* `gender`: The gender the person (e.g. 0).

### Dependencies ### 
`pt_name_gen` requires the `unidecode` library to remove special characters from the generated names.

### License ###

The `pt_name_gen` module is released under the MIT License.

I hope this helps! Let me know if you have any questions.