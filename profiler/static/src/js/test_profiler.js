(function(){
    'use_strict';
    openerp.Tour.register({
        id: 'profile_run',
        name: 'Profile run',
        path: '/web',
        model: 'test',
        steps: [
            {
                title: 'Enable profile',
                element: 'form:has(class(title="Start profiling")) a.a-submit',
                waitFor: 'console("ok")',
            },
        ],
    });
}());
