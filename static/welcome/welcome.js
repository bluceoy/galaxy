// document.addEventListener('DOMContentLoaded', function() {
//   let elems = document.querySelectorAll('.pushpin-nav');
//   let options = [...elems].map((elem) => {
//     let $target = $('#' + elem.dataset.target);
//     return {
//       top: $target.offset().top,
//       bottom: $target.offset().top + $target.outerHeight() - elem.clientHeight
//     }
//   })
//   let instances = M.Pushpin.init(elems, options);
// });

$(document).ready(function(){
  $('.collapsible').collapsible();
  $('.scrollspy').scrollSpy({scrollOffset: 64});
  $('.materialboxed').materialbox();
  $('.pushpin').pushpin();

  $('.pushpin-nav').each(function() {
    let $this = $(this);
    let $target = $('#' + $(this).attr('data-target'));
    $this.pushpin({
      top: $target.offset().top,
      bottom: $target.offset().top + $target.outerHeight() - $this.height()
    });
  });

  $(window).resize(function () {
    $('.pushpin-nav').each(function() {
      let $this = $(this);
      let $target = $('#' + $(this).attr('data-target'));
      $this.pushpin({
        top: $target.offset().top,
        bottom: $target.offset().top + $target.outerHeight() - $this.height()
      });
    });
  })

  //collapsible-header changes top and bottom, modify setting accordingly
  $('.collapsible-header').on("click", function () {
    let target = $(this);
    setTimeout(()=> {
      $('.pushpin-nav').each(function() {
        let $this = $(this);
        let $target = $('#' + $(this).attr('data-target'));
        $this.pushpin({
          top: $target.offset().top,
          bottom: $target.offset().top + $target.outerHeight() - $this.height()
        });
      });
    }
    ,500)
  })
});

window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 700 || document.documentElement.scrollTop > 700) {
    document.getElementById("topBtn").style.display = "block";
  } else {
    document.getElementById("topBtn").style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function toTop() {
  document.body.scrollTop = 0; // For Safari
  document.documentElement.scrollTop = 0; // For Chrome, Firefox, IE and Opera
}


// function pushpinNavRecalc() {
  
//   $('.pushpin-nav').each(() => {
//     let $this = $(this);
//     let $target = $('#' + $(this).attr('data-target'));
//     let instance = M.Pushpin.getInstance($target)
//     debugger;

    
//     $this.pushpin({
//       top: $target.offset().top,
//       bottom: $target.offset().top + $target.outerHeight() - $this.height()
//     })
//   })
  
  
  // $("your-element").pushpin({
  //     //update the properties
  //     top: /*recalculate value*/,
  //     bottom: /*recalculate value*/,
  //     offset: /*recalculate value*/
  // });


  // $('.pushpin-nav').each(function() {
    
  //   );
  // })
// }


//I update the values on window resize, I guess you can bind this to every change you need but haven't tested
// $( window ).resize(pushpinNavRecalc);