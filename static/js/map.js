document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadAttractions();
});

var map;  // Global map variable
var mapMarkers = {};  // To store markers for easy access and manipulation
var currentSelected = null;  // To track the currently selected list item

function initializeMap() {
    map = L.map('map').setView([mapData.center.lat, mapData.center.lon], 16);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap'
    }).addTo(map);

    map.on('moveend', function() {
        updateURL();
    });
}
function updateURL() {
    if (map) {
        var center = map.getCenter();
        var zoom = map.getZoom();
        window.location.hash = `lat=${center.lat.toFixed(6)}&lng=${center.lng.toFixed(6)}&zoom=${zoom}`;
    }
}

function loadAttractions() {
    mapData.attractions.forEach(function(attraction) {
        var marker = L.marker([attraction.coordinate.lat, attraction.coordinate.lon]);
        marker.addTo(map).bindPopup(
            `<h6 class="m-0">${attraction.name}</h6>
            <p>${attraction.description}</p>
            <button class="btn btn-sm btn-primary" onclick="toggleRoute('${attraction.id}', '${attraction.name}', this)">加入路线</button>`
            
            );

        // Store marker reference in mapMarkers dictionary
        mapMarkers[attraction.id] = marker;

        // Add event listener to marker
        marker.on('click', function() {
            selectAttraction(attraction.id);
        });

        // Add attractions to list
        var list = document.getElementById('attraction-list');
        var listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.textContent = attraction.name;
        listItem.setAttribute('data-id', attraction.id);
        listItem.onclick = function() {
            selectAttraction(attraction.id);
        };
        list.appendChild(listItem);
    });
}

function selectAttraction(id) {
    if (currentSelected) {
        if (currentSelected.marker) {
            currentSelected.marker.closePopup(); // 关闭当前打开的弹窗
        }
        if (currentSelected.listItem) {
            currentSelected.listItem.classList.remove('active'); // 移除当前高亮的列表项
        }
    }

    // 检索地图标记和列表项
    var marker = mapMarkers[id];
    var listItem = document.querySelector(`li[data-id="${id}"]`);

    if (listItem) {
        listItem.classList.add('active'); // 高亮新的列表项
        // 确保列表项在侧边栏可视区域内
        listItem.scrollIntoView({behavior: 'smooth', block: 'center'});
    }
    if (marker) {
        marker.openPopup(); // 为地图标记打开弹窗
    }

    // 更新当前选中对象
    currentSelected = { marker: marker, listItem: listItem };
}


function toggleRoute(id, name, btn) {
    var routeList = document.getElementById('route-list');
    var exists = routeList.querySelector(`li[data-id="${id}"]`);
    if (!exists) {
        // 检查是否已经存在于路线中，如果不在则添加
        var listItem = document.createElement('li');
        listItem.textContent = name;
        listItem.setAttribute('data-id', id);
        listItem.className = 'list-group-item d-flex justify-content-between align-items-center';

        var closeButton = document.createElement('button');
        closeButton.className = 'btn-close';
        closeButton.setAttribute('onclick', `removeFromRoute('${id}', this.parentElement)`);
        listItem.appendChild(closeButton);

        routeList.appendChild(listItem);
        btn.textContent = '移出路线';
        setActiveTab('routing'); // 切换到路径规划标签
    } else {
        // 如果已在路线中，则移除
        exists.remove();
        btn.textContent = '加入路线';
    }
}

function setActiveTab(tabId) {
    var tab = document.getElementById(tabId + '-tab');
    var pill = new bootstrap.Tab(tab);
    pill.show();  // Bootstrap 5 tab show method
}

function removeFromRoute(id, listItem) {
    listItem.remove();
    // 更新按钮文本（如果需要可以找到对应的按钮并更新其文本）
    var button = document.querySelector(`button[onclick*="toggleRoute('${id}'"]`);
    if (button) {
        button.textContent = '加入路线';
    }
}

function searchFood() {
    var searchType = document.getElementById('food-search-type').value;
    var searchText = document.getElementById('food-search-input').value;
    var sortOption = document.getElementById('restaurant-sort').value;
    var cuisineOption = document.getElementById('cuisine-filter').value;

    // 在这里实现调用后端 API 的 AJAX 请求，发送这些参数并更新餐馆列表
    // 以下是示例逻辑：
    console.log(searchType, searchText, sortOption, cuisineOption);
    // 实际的 AJAX 请求将根据您的后端 API 调整
}


