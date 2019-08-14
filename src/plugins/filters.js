import {format, parse} from 'date-fns'

export function install(Vue, options) {

    Vue.filter('datetime', function(value) {
      return format(parse(value), 'YYYY/MM/DD HH:mm')
    })

}

export default {install}
