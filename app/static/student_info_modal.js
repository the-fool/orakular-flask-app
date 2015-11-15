$(document).ready(function() {
    $('tr.student-info').click(function() {
	var id=$(this).data('id');
	var name=$(this).children().eq(1).text();
	console.log(name);
	$('#student_info').data('id', id);
	$('#student_info .modal-title').text(name);
	$('#student_info .modal-body').load('/ajax/student_modal?sid='+id, function() {
	  $('.student-info-course-tab', $('#student-info-tabs')).each(function() {
	      var total = 0;
	      $('.grade', $(this)).each(function() {
		  console.log(total);
		  total += parseFloat($(this).text());
	      });
	      $('.course-avg', $(this)).text( (total / 3).toPrecision(3));
	  });
	     
	});
	$('#student_info').modal('show');
    });
});
