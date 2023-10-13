// 임의의 게시글 데이터 (번호, 제목, 조회수, 추천수)
const posts = [
  { id: 1, title: '추장보다 높은 사람은?', views: 100, likes: 10 },
  { id: 2, title: '차가 다니는 도로에 갑자기 사람이 뛰어들면?', views: 200, likes: 15 },
  // 게시글
];

let currentPage = 1;
let perPage = 5;

function renderPosts() {
  const boardElement = document.getElementById('board');
  boardElement.innerHTML = '';
  const startIndex = (currentPage - 1) * perPage;
  const endIndex = startIndex + perPage;
  const currentPosts = posts.slice(startIndex, endIndex);

  for (const post of currentPosts) {
    const postElement = document.createElement('div');
    postElement.innerHTML = `
        <span>${post.id}</span>
        <a href="#" onclick="goToPost(${post.id})">${post.title}</a>
        <span>${post.views} views</span>
        <span>${post.likes} likes</span>
      `;
    boardElement.appendChild(postElement);
  }
}

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

// function goToPost(postId) {
//   // TODO: 게시글 상세 페이지로 이동
// }

// function goToWritePage() {
//   // TODO: 게시글 작성 페이지로 이동
// }

// 초기 렌더링
renderPosts();
renderPagination();
