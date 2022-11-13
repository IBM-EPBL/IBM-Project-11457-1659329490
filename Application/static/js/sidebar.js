(function ($) {
  "use strict";
  $(function () {
    $('[data-bs-toggle="offcanvas"]').on("click", function () {
      $(".sidebar-offcanvas").toggleClass("active");
    });
  });
})(jQuery);

(function ($) {
  "use strict";
  $(function () {
    //checkbox and radios
    $(".form-check label,.form-radio label").append(
      '<i class="input-helper"></i>'
    );
  });
})(jQuery);
