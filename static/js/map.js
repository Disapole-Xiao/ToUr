var map;  // Global map variable
var mapMarkers = {};  // To store markers for easy access and manipulation
var currentSelected = null;  // To track the currently selected list item
var routeLayer = L.layerGroup();

// 自定义Icon
var entranceIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
var attractionIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
var amenityIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
var restaurantIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

// 当网页加载完成时启动
document.addEventListener('DOMContentLoaded', function() {
    initializeMap();
    loadAttractions();
    // 标记出入口点
    entrance_node_id = mapData.entrance;
    entrance = mapData.nodes[entrance_node_id];
    L.marker([entrance.lat, entrance.lon], {icon: entranceIcon}).addTo(map).bindPopup(
        `<h6 class="m-0">入口</h6>`
    );
    drawRoads(); // 画道路
    routeLayer.addTo(map)
});

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
function setActiveTab(tabId) {
    var tab = document.getElementById(tabId + '-tab');
    var pill = new bootstrap.Tab(tab);
    pill.show();  // Bootstrap 5 tab show method
}

//--------- 景点页面相关函数 ------------
function loadAttractions() {
    mapData.attractions.forEach(function(attraction) {
        var marker = L.marker([attraction.coordinate.lat, attraction.coordinate.lon]);
        marker.addTo(map).bindPopup(function() {
            // Determine button text based on current route list status
            var routeList = document.getElementById('route-list');
            var exists = routeList.querySelector(`li[data-id="${attraction.id}"]`);
            var buttonText = exists ? '移出路线' : '加入路线';
            
            return `<h6 class="m-0">${attraction.name}</h6>
                    <p>${attraction.description}</p>
                    <button class="btn btn-sm btn-primary" onclick="toggleRoute('${attraction.id}', '${attraction.name}', this)">${buttonText}</button>`;
        });

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
        listItem.setAttribute('data-id', attraction.id); // 列表的data_id就是景点的id
        listItem.onclick = function() {
            selectAttraction(attraction.id);
        };
        list.appendChild(listItem);
    });
}


function drawRoads() {
    mapData.nodes.forEach(function(node) {
        node.adj.forEach(function(adj) {
            var adjNode_id = adj.id; 
            var adjNode = mapData.nodes[adjNode_id];
            if (adjNode) {
                var color = adj.bicycle ? 'green' : 'gray';
                var polyline = L.polyline(
                    [[node.lat, node.lon], [adjNode.lat, adjNode.lon]], 
                    {
                        color: color,
                        weight: 5,
                        // opacity: adj.congestion
                    }
                ).addTo(map);
                polyline.bindPopup("<div>congestion:" + adj.congestion + "<br>distance:" + adj.distance + "</div>");
            }
        });
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

//------------ 路径规划页面相关函数 -----------
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
function removeFromRoute(id, listItem) {
    listItem.remove();
    // 更新按钮文本（如果需要可以找到对应的按钮并更新其文本）
    var button = document.querySelector(`button[onclick*="toggleRoute('${id}'"]`);
    if (button) {
        button.textContent = '加入路线';
    }
}

// 当点击“规划路径”按钮时触发的函数
function planRoute(mode) {
    // 1. 获取当前加入路线的景点列表
    var routeList = document.getElementById('route-list');
    var selected_attractions = [];
    routeList.querySelectorAll('li').forEach(li => {
        selected_attractions.push(li.getAttribute('data-id'));
    });
    console.log(selected_attractions);
    // 2. 调用后端函数发送请求，并处理返回的 JSON 数据
    fetch('plan_route/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // 将 CSRF 令牌包含在请求头中
        },
        body: JSON.stringify({ selected_attractions: selected_attractions, mode: mode }),
    })
    .then(response => response.json())
    .then(data => {
        // 3. 在地图上绘制路径
        var latLonSeq = data.latLonSeq;
        console.log(latLonSeq);
        displayRoute(latLonSeq);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 在页面上展示路径信息的函数
// function displayRouteInfo(data) {
//     var routeInfoDiv = document.getElementById('planned-routes');
//     routeInfoDiv.innerHTML = ''; // 清空原有内容

//     // 创建并添加新的路线信息
//     data.routes.forEach(route => {
//         var routeItem = document.createElement('div');
//         routeItem.textContent = route;
//         routeInfoDiv.appendChild(routeItem);
//     });
// }


// 在地图上绘制路径的函数
function displayRoute(latLonSeq) {
    console.log(latLonSeq);
    routeLayer.clearLayers(); // 清除之前的路径图层
    routeLayer.addLayer(
        L.polyline(latLonSeq, {
        color: 'red',
        weight: 6,
        dashArray: '5, 10',
    }))
    console.log('finish');
    
    
}



// -------------------------------------
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


