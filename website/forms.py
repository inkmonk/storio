from flask.ext.security.forms import Form, NextFormMixin, get_form_field_label
from wtforms import TextField, PasswordField, SubmitField, BooleanField
from flask import request
from flask.ext.security.utils import (
    get_message, verify_and_update_password, encrypt_password)
from .models import User


class LoginForm(Form, NextFormMixin):
    """The default login form"""

    name = TextField(get_form_field_label('name'))
    password = PasswordField(get_form_field_label('password'))
    remember = BooleanField(get_form_field_label('remember_me'))
    submit = SubmitField(get_form_field_label('login'))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.remember.data = True
        self.name.errors = []
        self.password.errors = []
        if not self.next.data:
            self.next.data = request.args.get('next', '')

    def validate(self):
        print "in validate"
        # if not super(LoginForm, self).validate():
        #     print "False1"
        #     return False

        if self.name.data.strip() == '':
            print "False2"
            self.name.errors.append(get_message('NAME_NOT_PROVIDED')[0])
            return False

        if self.password.data.strip() == '':
            self.password.errors.append(
                get_message('PASSWORD_NOT_PROVIDED')[0])
            return False

        self.user = User.first(name=self.name.data)
        if self.user is None:
            self.user = User.create(
                name=self.name.data, active=True,
                password=encrypt_password(self.password.data))
            return True
        print "got user as %s" % self.user

        if self.user is None:
            self.name.errors.append(get_message('USER_DOES_NOT_EXIST')[0])
            return False
        if not self.user.password:
            print self.password.errors
            self.password.errors.append(get_message('PASSWORD_NOT_SET')[0])
            return False
        if not verify_and_update_password(self.password.data, self.user):
            print self.password.errors
            self.password.errors.append(get_message('INVALID_PASSWORD')[0])
            return False
        return True
