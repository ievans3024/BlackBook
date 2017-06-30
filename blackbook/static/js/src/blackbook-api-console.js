"use strict";

let Cookies = {

  _parse () {

    let mapping = {};

    document.cookie.split('; ').forEach(
      (c) => {
        let split = c.split('=', 1);
        mapping[split[0]] = split[1];
      }
    );

    return mapping;

  },

  get (name) {
    return this._parse()[name];
  },

  set (name, value) {
    document.cookie = [name, value].join('=');
    return this._parse()[name];
  }

};

function get_xsrf_token() {
  return Cookies.get('XSRF-Token').replace('s:','').replace(/\..+/,'');
}

class APIConsole {

  constructor () {
    let token = get_xsrf_token();
    this.xsrf = token ? {token: token} : {};
  }

  createResource (href, data) {
    let xhr_opts = {
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data)
    };
    if (this.xsrf.token !== undefined) {
      xhr_opts.headers = {
        'X-XSRF-Token': this.xsrf.token
      }
    }
    return jQuery.ajax(href, xhr_opts);
  }

  updateResource (href, data) {
    return jQuery.ajax(
      href,
      {
        method: 'PATCH',
        headers: {
          'X-XSRF-Token': this.xsrf.token
        },
        contentType: 'application/json',
        data: JSON.stringify(data)
      }
    );
  }

  getResource (href) {
    return jQuery.ajax(
      href,
      {
        method: 'GET',
        headers: {
          'X-XSRF-Token': this.xsrf.token
        },
        contentType: 'application/json'
      }
    );
  }

  deleteResource (href) {
    return jQuery.ajax(
      href,
      {
        method: 'DELETE',
        headers: {
          'X-XSRF-Token': this.xsrf.token
        },
        contentType: 'application/json'
      }
    );
  }

  login (href, email, password) {
    let self = this;
    return jQuery.ajax(
      href,
      {
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({email: email, password: password})
      }
    )
      .done(
        () => {
          this.xsrf.token = get_xsrf_token();
        }
      );
  }

  logout (href) {
    return jQuery.ajax(
      href,
      {
        method: 'DELETE',
        contentType: 'application/json',
        headers: {
          'X-XSRF-Token': this.xsrf.token
        }
      }
    )
      .done(
        () => {
          delete this.xsrf.token;
        }
      );
  }

}