let currentPage = 1;
let perPage = 5;

function renderPosts() {
  const boardElement = document.getElementById('board');
  boardElement.innerHTML = '';
  const startIndex = (currentPage - 1) * perPage;
  const endIndex = startIndex + perPage;

function renderPagination() {
  const paginationElement = document.getElementById('pagination');
  paginationElement.innerHTML = '';
  const totalPages = Math.ceil(posts.length / perPage);
  const maxDisplayedPages = 10;
  const startPage = Math.max(1, currentPage - Math.floor(maxDisplayedPages / 2));
  const endPage = Math.min(totalPages, startPage + maxDisplayedPages - 1);

  for (let page = startPage; page <= endPage; page++) {
    const pageElement = document.createElement('span');
    pageElement.innerHTML = `<a href="#" onclick="changePage(${page})">${page}</a>`;
    paginationElement.appendChild(pageElement);
  }
}

function changePerPage() {
  perPage = parseInt(document.getElementById('perPage').value);
  currentPage = 1;
  renderPosts();
  renderPagination();
}

function sortByRecommend() {
  posts.sort((a, b) => b.likes - a.likes);
  currentPage = 1;
  renderPosts();
  renderPagination();
}

function sortByNewest() {
  posts.sort((a, b) => b.id - a.id);
  currentPage = 1;
  renderPosts();
  renderPagination();
}

function sortByOldest() {
  posts.sort((a, b) => a.id - b.id);
  currentPage = 1;
  renderPosts();
  renderPagination();
}

function changePage(page) {
  currentPage = page;
  renderPosts();
  renderPagination();
}

// 초기 렌더링
renderPosts();
renderPagination();
