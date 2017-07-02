(function(){
    'use_strict';
    openerp.Tour.register({
        id: 'profile_run',
        name: 'Profile run',
        path: '/web',
        mode: 'test',
        steps: [
            {
                title: 'Start profiling',
                element: 'a.profiler_enable'
            },
            {
                title: 'Check enabled',
                waitFor: 'li.oe_topbar_item.profiler_player.profiler_player_enabled'
            },
            {
                title: 'Stop profiling',
                element: 'a.profiler_disable'
            },
            {
                title: 'Check disabled',
                waitFor: 'li.oe_topbar_item.profiler_player.profiler_player_disabled'
            },
            {
                title: 'Dump profiling',
                element: 'a.profiler_dump'
            },
            {
                title: 'Clear profiling',
                element: 'a.profiler_clear'
            }
        ]
    });
}());
