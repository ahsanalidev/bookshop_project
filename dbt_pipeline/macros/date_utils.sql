-- macro to get year from input_date
{% macro get_year(input_date) %}
    extract(year from {{ input_date }})
{% endmacro %}

-- macro to convert input_date to french month
{% macro get_french_month(input_date) %}
    case
        when date_part('month', {{ input_date }}) = 1 then 'Janvier'
        when date_part('month', {{ input_date }}) = 2 then 'Février'
        when date_part('month', {{ input_date }}) = 3 then 'Mars'
        when date_part('month', {{ input_date }}) = 4 then 'Avril'
        when date_part('month', {{ input_date }}) = 5 then 'Mai'
        when date_part('month', {{ input_date }}) = 6 then 'Juin'
        when date_part('month', {{ input_date }}) = 7 then 'Juillet'
        when date_part('month', {{ input_date }}) = 8 then 'Août'
        when date_part('month', {{ input_date }}) = 9 then 'Septembre'
        when date_part('month', {{ input_date }}) = 10 then 'Octobre'
        when date_part('month', {{ input_date }}) = 11 then 'Novembre'
        when date_part('month', {{ input_date }}) = 12 then 'Décembre'
    end
{% endmacro %}

-- macro to convert input_date to french day
{% macro get_french_day(input_date) %}
    case
        when date_part('dayofweek', {{ input_date }}) = 0 then 'Dimanche'  
        when date_part('dayofweek', {{ input_date }}) = 1 then 'Lundi'
        when date_part('dayofweek', {{ input_date }}) = 2 then 'Mardi'
        when date_part('dayofweek', {{ input_date }}) = 3 then 'Mercredi'
        when date_part('dayofweek', {{ input_date }}) = 4 then 'Jeudi'
        when date_part('dayofweek', {{ input_date }}) = 5 then 'Vendredi'
        when date_part('dayofweek', {{ input_date }}) = 6 then 'Samedi'
    end
{% endmacro %}
