from flask import render_template, flash, redirect, url_for, make_response
from app import app
from app.forms import CompareDatesForm
from pathlib import Path

from app import utils

REGIONS_CONFIG = {
    'sochi': {
        'code': '23',
        'name': 'Сочи',
        'id': 'sochi',
        'function': utils.sochi,
        'text': ''
    },
    'bryansk': {
        'code': '32',
        'name': 'Брянск',
        'id': 'bryansk',
        'function': utils.bryansk,
        'text': ''
    },
    'bryansk-obl': {
        'code': '32',
        'name': 'Брянская автоколонна №1403',
        'id': 'bryansk-obl',
        'function': utils.bryansk_obl,
        'text': ''
    },
    'smolensk': {
        'code': '67',
        'name': 'Смоленск',
        'id': 'smolensk',
        'function': utils.smolensk,
        'text': ''
    },
    'tambov': {
        'code': '68',
        'name': 'Тамбов',
        'id': 'tambov',
        'function': utils.tambov,
        'text': ''
    },
    'tula' : {
        'code': '71',
        'name': 'Тула',
        'id': 'tula',
        'function': utils.tula,
        'text': ''
    },
    'tyumen': {
        'code': '72',
        'name': 'Тюмень',
        'id': 'tyumen',
        'function': utils.tyumen,
        'text': ''
    }
}

@app.route('/')
@app.route('/index')
def index():
    regions = list(REGIONS_CONFIG.values())
    return render_template('index.html', title='home', regions=regions)

@app.route('/<region_id>')
def region_page(region_id):
    region_config = REGIONS_CONFIG[region_id]
    form = CompareDatesForm()
    choices = utils.get_available_dates(region_config)
    if not choices:
        choices = []
    form.date1.choices = choices
    form.date2.choices = choices
    return render_template('region.html', title=region_config['name'], region=region_config, form=form, differences=None, new=None)

@app.route('/<region_id>/file/<path:filepath>')
def serve_file(region_id, filepath):
    full_path = Path('data/regions') / region_id / filepath
    if not full_path.exists():
        flash('Файл не найден', 'alert alert-warning')
        return redirect(url_for('region_page', region_id=region_id))
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    response = make_response(content)
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response

@app.route('/<region_id>/update')
def update(region_id):
    region_config = REGIONS_CONFIG[region_id]
    try:
        region_config['function']()
        flash('Расписание успешно обновлено', 'alert alert-info')
    except Exception as e:
        flash(f'Ошибка при обновлении: {str(e)}', 'alert alert-danger')
    return redirect(url_for('region_page', region_id=region_id))

@app.route('/<region_id>/compare', methods=['POST', 'GET'])
def compare(region_id):
    region_config = REGIONS_CONFIG[region_id]

    form = CompareDatesForm()
    choices = utils.get_available_dates(region_config)
    form.date1.choices = choices
    form.date2.choices = choices
    if form.validate_on_submit():
        date1 = form.date1.data
        date2 = form.date2.data
        if date1 != date2:
            differences, new = utils.compare_dirs(date1, date2, region_config)
            return render_template('region.html', title=region_config['name'], region=region_config, form=form, differences=differences, new=new)
        else:
            flash('Указаны одинаковые даты', 'alert alert-warning')
    return render_template('region.html', title=region_config['name'], region=region_config, form=form, differences=None, new=None)

