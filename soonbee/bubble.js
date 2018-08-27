describe("Bubble Test", function() {
  var arr;

  before("Create the array", function() {
    arr = [2, 1, 6, 7, 4, 3];
  });

  after("Destory the array", function() {
    arr = undefined;
  });

  it("test complete", function() {
    for (let i = 0; i < arr.length - 1; i++) {
      for (let j = i; j < arr.length - 1; j++) {
        if (arr[j] > arr[j + 1]) swap(j, j + 1);
      }
    }
    console.log(arr);
  });

  function swap(a, b) {
    const tmp = arr[a];
    arr[a] = arr[b];
    arr[b] = tmp;
  }
});
