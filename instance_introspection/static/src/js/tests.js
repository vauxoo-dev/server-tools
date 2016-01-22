(function() {
    'use strict';
    openerp.Tour.register({
        id: 'test_instance_introspection',
        name: 'Complete a basic order trough the Front-End',
        path: '/instance_introspection',
        mode: 'test',
        steps: [
            {
                title: 'Wait for the main screen',
                waitFor: 'h3:contains("Addons Paths"),#accordion.results',
            },
            {
                title:     'increase defaultDelay',
                onload: function (tour) {
                    openerp.Tour.defaultDelay = 5000;
                }
            },
            {
                title:  'Load Repositories',
                element: '.btn-reload',
            },
            {
                title:     'decrease defaultDelay',
                onload: function (tour) {
                    openerp.Tour.defaultDelay = 50;
                }
            },
            {
                title:  'Load Repositories',
                waitFor: '#accordion.results',
            },
        ],
    });

    openerp.Tour.register({
        id: 'test_pyinfo',
        name: 'Complete a basic order trough the Front-End',
        path: '/instance_introspection/pyenv',
        mode: 'test',
        steps: [
            {
                title: 'Wait for the main screen',
                waitFor: '.table',
            },
        ],
    });

    openerp.Tour.register({
        id: 'test_pyinfo_json',
        name: 'Complete a basic order trough the Front-End',
        path: '/instance_introspection.json',
        mode: 'test',
        steps: [
            {
                title: 'Wait for the main screen',
                waitFor: '.table',
            },
        ],
    });
})();

