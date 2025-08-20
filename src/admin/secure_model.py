from flask_admin.contrib.sqla import ModelView
from wtforms.fields import SelectField


class SecureModelView(ModelView):
    column_display_pk = True
    column_display_all_relations = True

    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

    def scaffold_form(self):
        """
        Override default form to show human-friendly dropdowns for foreign keys.
        """
        form_class = super().scaffold_form()

        for name, column in self.model.__table__.columns.items():
            if column.foreign_keys:
                fk = list(column.foreign_keys)[0]
                related_model = fk.column.table
                related_class = self.session.bind.mapper.registry._class_for_table(
                    related_model)

                # Try to find a human-friendly field to display
                display_attr = None
                for candidate in ["name", "username", "title", "email"]:
                    if hasattr(related_class, candidate):
                        display_attr = candidate
                        break

                # Default to primary key if no human-friendly attr is found
                if display_attr is None:
                    display_attr = "id"

                # Replace field with dropdown of human-friendly labels
                choices = [
                    (str(obj.id), getattr(obj, display_attr))
                    for obj in self.session.query(related_class).all()
                ]
                form_class.__dict__[name] = SelectField(name, choices=choices)

        return form_class
