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
                onload: function () {
                    $('a.profiler_enable').trigger('click');
                }
            },
            {
                title: 'Stop profiling',
                onload: function () {
                    $('a.profiler_disable').trigger('click');
                }

            },
            {
                title: 'Dump profiling',
                onload: function () {
                    $('a.profiler_dump').trigger('click');
                }
            },
            {
                title: 'Clear profiling',
                onload: setTimeout(function () {
                    $('a.profiler_clear').trigger('click');
                }, 2000)
            },

        ]
    });
}());
