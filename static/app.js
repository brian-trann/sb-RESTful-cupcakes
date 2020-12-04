$(async function() {
	const cupcakes = await loadCupcakes();
	// console.log(cupcakes);
	const cupcakeList = generateCupcakeHTML(cupcakes);
	$('.cupcake-holder').append(cupcakeList);

	$('.cupcake-form').on('submit', async function(event) {
		event.preventDefault();
		const cupcake = getCupcakeForm();

		await postCupcakes(cupcake);
		const newCupcakes = await loadCupcakes();
		const newCupcakeList = generateCupcakeHTML(newCupcakes);
		$('.cupcake-holder').empty().append(newCupcakeList);
		$('.cupcake-form').trigger('reset');
	});
});
async function loadCupcakes() {
	const cupcakes = await axios.get('/api/cupcakes');
	return cupcakes.data.cupcakes;
}
function generateCupcakeHTML(cupcakes) {
	$cupcakeList = $('<ul>');
	for (let cupcake of cupcakes) {
		const $cupcake = $(`<li>${cupcake.flavor}</li>`);
		$cupcakeList.append($cupcake);
	}
	return $cupcakeList;
}
function getCupcakeForm() {
	const flavor = $('#flavor').val();
	const size = $('#size').val();
	const rating = $('#rating').val();
	const image = $('#image').val();
	return { flavor, size, rating, image };
}
async function postCupcakes(cupcake) {
	const res = await axios({
		url    : '/api/cupcakes',
		method : 'POST',
		data   : {
			flavor : cupcake.flavor,
			rating : cupcake.rating,
			size   : cupcake.size,
			image  : cupcake.image
		}
	});
	return res;
}
