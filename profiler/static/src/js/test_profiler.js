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
                title: 'Check if is enabled',
                waitFor: 'li.oe_topbar_item.profiler_player.profiler_player_enabled'
            },
            {
                title: 'Disable profile',
                element: 'a.profiler_disable'
            },
            {
                title: 'Check if is disabled',
                waitFor: 'li.oe_topbar_item.profiler_player.profiler_player_disabled'
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
