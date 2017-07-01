(function(){
    'use_strict';
    openerp.Tour.register({
        id: 'profile_run',
        name: 'Profile run',
        path: '/web',
        mode: 'test',
        steps: [
            {
                title: 'Enable profile',
                element: 'a.profiler_enable'
            },
            {
                title: 'Disable profile',
                element: 'a.profiler_disable'
            },
            {
                title: 'Dump profile',
                element: 'a.profiler_dump'
            },
            {
                title: 'Clear profile',
                element: 'a.profiler_clear'
            },
        ]
    });
}());
