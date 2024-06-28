#!/usr/bin/python3
""" Console Module """
import cmd
import sys
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    classes = {
               'BaseModel': BaseModel, 'User': User, 'Place': Place,
               'State': State, 'City': City, 'Amenity': Amenity,
               'Review': Review
              }
    dot_cmds = ['all', 'count', 'show', 'destroy', 'update']
    types = {
             'number_rooms': int, 'number_bathrooms': int,
             'max_guest': int, 'price_by_night': int,
             'latitude': float, 'longitude': float
            }

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        _cmd = _cls = _id = _args = ''  # initialize line elements

        # scan for general formating - i.e '.', '(', ')'
        if not ('.' in line and '(' in line and ')' in line):
            return line

        try:  # parse line left to right
            pline = line[:]  # parsed line

            # isolate <class name>
            _cls = pline[:pline.find('.')]

            # isolate and validate <command>
            _cmd = pline[pline.find('.') + 1:pline.find('(')]
            if _cmd not in HBNBCommand.dot_cmds:
                raise Exception

            # if parantheses contain arguments, parse them
            pline = pline[pline.find('(') + 1:pline.find(')')]
            if pline:
                # partition args: (<id>, [<delim>], [<*args>])
                pline = pline.partition(', ')  # pline convert to tuple

                # isolate _id, stripping quotes
                _id = pline[0].replace('\"', '')
                # possible bug here:
                # empty quotes register as empty _id when replaced

                # if arguments exist beyond _id
                pline = pline[2].strip()  # pline is now str
                if pline:
                    # check for *args or **kwargs
                    if pline[0] == '{' and pline[-1] == '}' and type(eval(pline)) is dict:
                        _args = pline
                    else:
                        _args = pline.replace(',', '')
                        # reformat _args into list of args
                        _args = _args.replace('\"', '')
            line = ' '.join([_cmd, _cls, _id, _args])

        except Exception as mess:
            pass
        finally:
            return line

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, arg):
        """ Exit the HBNB console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, arg):
        """ Create an object of any class"""
        args = shlex.split(arg)
        if len(args) == 0:
            print("** class name missing **")
            return
        elif args[0] not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        cls_name = args[0]
        new_instance = HBNBCommand.classes[cls_name]()
        for param in args[1:]:
            key, value = param.split('=')
            if value[0] == '"':
                value = value.strip('"').replace('_', ' ')
            elif '.' in value:
                value = float(value)
            else:
                try:
                    value = int(value)
                except ValueError:
                    pass  # Keeps the value as a string if it can't be converted to int
            setattr(new_instance, key, value)
        storage.new(new_instance)
        storage.save()
        print(new_instance.id)

    def do_show(self, args):
        """ Show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all()[key])
        except KeyError:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Destroy a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if not c_name:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            storage.delete(storage.all()[key])
            storage.save()
        except KeyError:
            print("** no instance found **")

    def do_all(self, arg):
        """ Show all objects, or all objects of a class"""
        print_list = []
        if arg:
            args = arg.split(' ')
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            for k, v in storage.all(HBNBCommand.classes[args[0]]).items():
                print_list.append(str(v))
        else:
            for k, v in storage.all().items():
                print_list.append(str(v))
        print(print_list)

    def do_update(self, args):
        """ Update an object if exists """
        c_name, c_id, att_name, att_val = '', '', '', ''
        args = args.partition(" ")
        if args[0]:
            c_name = args[0]
        if args[2]:
            args = args[2].partition(" ")
            if args[0]:
                c_id = args[0]
            if args[2]:
                args = args[2].partition(" ")
                if args[0]:
                    att_name = args[0]
                if args[2]:
                    att_val = args[2]

        # guard against trailing args
        if att_val and ' ' in att_val:
            att_val = att_val.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return
        if c_name not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        if not c_id:
            print("** instance id missing **")
            return
        key = c_name + "." + c_id
        try:
            obj = storage.all()[key]
        except KeyError:
            print("** no instance found **")
            return
        if not att_name:
            print("** attribute name missing **")
            return
        if not att_val:
            print("** value missing **")
            return

        if att_name in HBNBCommand.types:
            try:
                att_val = HBNBCommand.types[att_name](att_val)
            except ValueError:
                print("** value type incorrect **")
                return

        setattr(obj, att_name, att_val)
        storage.save()

    def do_count(self, args):
        """ Count current number of class instances """
        if args:
            args = args.split(' ')
            if args[0] not in HBNBCommand.classes:
                print("** class doesn't exist **")
                return
            count = 0
            for k in storage.all(HBNBCommand.classes[args[0]]).keys():
                count += 1
            print(count)
        else:
            print("** class name missing **")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
