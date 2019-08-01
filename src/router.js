import Vue from 'vue'
import VueRouter from 'vue-router'

import store from './store'

Vue.use(VueRouter)

const router = new VueRouter({
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('./home/index.vue'),
      meta: { breadcrumb: 'Home' }
    },
    {
      path: '/:domain',
      component: () => import('./domain/index.vue'),
      meta: { breadcrumb: s => s.state.domain, default: 'domain' },
      beforeEnter(to, from, next) {
        store.dispatch('setDomain', to.params.domain).then(next);
      },
      children: [
        {
          path: '',
          name: 'domain',
          component: () => import('./domain/datatable.vue')
        },
        {
          path: ':date',
          component: () => import('./run/index.vue'),
          meta: { breadcrumb: s => s.getters.currentDate, default: 'run' },
          beforeEnter(to, from, next) {
            store.dispatch('setRun', to.params.date).then(next);
          },
          children: [
            {
              path: '',
              name: 'run',
              component: () => import('./run/datatable.vue')
            },
            {
              path: ':query',
              name: 'query',
              component: () => import('./query/index.vue'),
              meta: { breadcrumb: s => s.getters.currentQuery },
              beforeEnter(to, from, next) {
                store.dispatch('setQuery', to.params.query).then(next);
              }
            }
          ]
        }
      ]
    },

    // Error pages
    { path: '*', name: 'not-found', component: () => import('./error.vue') }
  ]
});

export default router
