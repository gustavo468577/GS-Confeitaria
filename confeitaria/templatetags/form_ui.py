from django import forms, template

register = template.Library()


@register.filter
def bootstrap_field(field):
    # Render existing widgets without changing validation, querysets or form behavior.
    widget = field.field.widget
    if isinstance(widget, forms.CheckboxInput):
        css = 'form-check-input'
    elif isinstance(widget, forms.FileInput):
        css = 'form-control-file'
    else:
        css = 'form-control'
    attrs = {'class': (widget.attrs.get('class', '') + ' ' + css).strip()}
    described_by = []
    if field.help_text:
        described_by.append(f'{field.auto_id}_helptext')
    if field.errors:
        attrs['class'] += ' is-invalid'
        attrs['aria-invalid'] = 'true'
        described_by.append(f'{field.auto_id}_errors')
    if described_by:
        attrs['aria-describedby'] = ' '.join(described_by)
    return field.as_widget(attrs=attrs)


@register.filter
def startswith(value, prefix):
    return bool(prefix) and str(value).startswith(str(prefix))
