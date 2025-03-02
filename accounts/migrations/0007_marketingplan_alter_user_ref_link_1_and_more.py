# Generated by Django 5.1.6 on 2025-02-24 10:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_activity_status_user_binary_balance_user_pv_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('partner_types', models.TextField(help_text='Введите типы партнеров через запятую (например: start, smart, senior, sovereign, stellar)', verbose_name='Типы партнеров')),
                ('qualification_types', models.TextField(help_text='Введите типы квалификаций через запятую (например: Status 0, Status 1, ..., Status 9)', verbose_name='Типы квалификаций')),
                ('activity_period', models.CharField(help_text='Введите диапазон активности (например: 2025-01-01 до 2025-12-31)', max_length=255, verbose_name='Период активности')),
                ('career', models.TextField(blank=True, help_text='Описание карьеры', null=True, verbose_name='Карьера')),
                ('team', models.TextField(blank=True, help_text='Описание команды', null=True, verbose_name='Команда')),
            ],
            options={
                'verbose_name': 'Маркетинговый план',
                'verbose_name_plural': 'Маркетинговые планы',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='ref_link_1',
            field=models.CharField(default='LpRQx1ySRYr9UR4g7udAymBIeCie6iZt', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='ref_link_2',
            field=models.CharField(default='KsewBHJ8ibLNvkX2vYs4peam2ygvUdaj', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='wallet_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Значение кошелька'),
        ),
        migrations.CreateModel(
            name='PortalSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header_logo', models.ImageField(upload_to='portal/logo/', verbose_name='Логотип')),
                ('footer_menu', models.ManyToManyField(blank=True, related_name='footer_menu_items', to='accounts.menuitem', verbose_name='Меню в футере')),
                ('header_menu', models.ManyToManyField(blank=True, related_name='header_menu_items', to='accounts.menuitem', verbose_name='Меню в хедере')),
            ],
            options={
                'verbose_name': 'Настройка портала',
                'verbose_name_plural': 'Настройки портала',
            },
        ),
    ]
