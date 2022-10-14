if (typeof _$ == "undefined") _$ = {};
window._$ = {
  async Fetch(url, isArray = false, props = {}) {
    let options = {
      method: "GET",
      ...props,
    };
    if (options.body) {
      options.body = JSON.stringify(options.body);
    }
    try {
      let res = await fetch(url, options);
      let json = await res.json();
      if (isArray) {
        return [res, json];
      }
      return json;
    } catch (err) {
      console.log(err);
      toastr.error(err);
      if (isArray) {
        return [false, false];
      }
      return false;
    }
  },
  crModal(title, body, type, large = false) {
    const elId = "body",
      id = ("integrated-modal-" + Math.random()).replace(".", ""),
      mContent = $('<div class="modal-content" />');

    if (title) {
      let mh = $(`<div class="modal-header" />`);
      mh.append($(`<h5 class="modal-title" />`).append(title));
      mh.append(
        $(
          `<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>`
        )
      );
      mContent.append(mh);
    }
    mContent.append($(`<div class="modal-body" />`).append($(body)));
    $(elId).append(
      $(`<div class="modal fade" id="${id}" data-backdrop="static" tabindex="-1" role="dialog" 
            aria-labelledby="staticBackdrop" aria-hidden="true">`).append(
        $(
          `<div class="modal-dialog modal-dialog-scrollable modal-dialog-centered ${
            type ? "modal-sm" : ""
          } ${large ? "modal-lg" : ""}" role="documnet" />`
        ).append(mContent)
      )
    );
    var scrollY = $("html, body").scrollTop();
    $("#" + id)
      .on("show.bs.modal", (_) => {
        $("html,body").animate({ scrollTop: scrollY });
      })
      .on("hidden.bs.modal", function () {
        $(this).remove();
      })
      .modal("show");
    return id;
  },
};
