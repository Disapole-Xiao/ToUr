var map;  // Global map variable
var attractionMarkers = {};  // To store markers for easy access and manipulation
var entranceMarker = null
var currentSelected = null;  // To track the currently selected list item

var routeLayer = L.layerGroup();
var amenityLayer = L.layerGroup();
var restaurantLayer = L.layerGroup();

const congestionColors = [
    '#fe5858',
    '#fe7058',
    '#fe8958',
    '#fea158',
    '#feba58',
    '#fed258',
    '#dbd357',
    '#b9d456',
    '#96d456',
    '#74d555',
    '#51d654',
   ];
    

// 自定义Icon
const entranceIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-black.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
const attractionIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-orange.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
const amenityIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
const restaurantIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-violet.png',
    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});
const highlightIcon = new L.Icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-gold.png',
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
    // 入口点
    loadEntrance();
    // 画道路
    drawRoads(); 
    // 加图层
    routeLayer.addTo(map)
    amenityLayer.addTo(map)
    restaurantLayer.addTo(map)
    // 增加事件监听器，点击设施标签时加载设施数据
    document.getElementById('amenities-tab').addEventListener('click', searchAmenity);
    document.getElementById('restaurants-tab').addEventListener('click', searchRestaurant);

    map.on('click', function(e) {
        // 此函数仅当点击地图空白处时调用
        selectAttraction(null);
    });
});

function initializeMap() {
    map = L.map('map', {
        center: [mapData.center.lat, mapData.center.lon],
        zoom: 16,
        zoomControl: false,
        zoomSnap: 0.5,
        zoomDelta: 0.5
    });
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap',
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
// function setActiveTab(tabId) {
//     var tab = document.getElementById(tabId + '-tab');
//     var pill = new bootstrap.Tab(tab);
//     pill.show();  // Bootstrap 5 tab show method
// }

function highlightListItem(listItem, marker) {
    // map.setView([amenity.lat, amenity.lon], 18);
    marker.openPopup();
    // 清除其他列表项的active
    var activeItem = document.querySelector('.list-group-item.active');
    if (activeItem) {
        activeItem.classList.remove('active');
    }
    
    listItem.classList.add('active'); // 高亮新的列表项
    listItem.scrollIntoView({behavior: 'smooth', block: 'center'}); // 确保列表项在侧边栏可视区域内
}
function updateCoord(arrName, id, marker) {
    lat = marker.getLatLng().lat;
    lon = marker.getLatLng().lng;
    fetch('update_coord/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // 将 CSRF 令牌包含在请求头中
        },
        body: JSON.stringify({ 'arr_name': arrName, 'id': id, 'lat': lat, 'lon': lon }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('坐标更新成功！');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function loadEntrance() {
    entrance_node_id = mapData.entrance;
    entrance = mapData.nodes[entrance_node_id];
    entranceMarker = L.marker([entrance.lat, entrance.lon], {
            icon: entranceIcon, 
            draggable: edit ? true : false,
            autoPan: edit ? true : false,
        }).addTo(map);
    entranceMarker.bindPopup(function() {
        var routeList = document.getElementById('route-list');
        var exists = routeList.querySelector(`li[data-id="-1"]`);
        var buttonText = exists ? '移出路线' : '加入路线';
    entranceMarker.on('dragend', function() {
        updateCoord('nodes', entrance_node_id, this)
    }
)  
        return `<h6 class="m-0">入口</h6>
                <p></p>
                <button class="btn btn-sm btn-primary" onclick="toggleRoute('-1', '入口', this)">${buttonText}</button>`;
    });
    entranceMarker.options.attractionId = -1; // 把入口当特殊景点处理
    entranceMarker.options.attractionName = "入口";
    entranceMarker.on('click', function(e) {
        e.originalEvent.stopPropagation();
        selectAttraction(-1);
    });
}
//--------- 景点页面相关函数 ------------
function loadAttractions() {
    mapData.attractions.forEach(function(attraction) {
        var marker = L.marker([attraction.lat, attraction.lon], {
            icon: attractionIcon,
            draggable: edit ? true : false,
            autoPan: edit ? true : false,
        });

        // 存储自定义数据
        marker.options.attractionId = attraction.id;  // 添加景点ID作为标记的自定义选项
        marker.options.attractionName = attraction.name;

        marker.addTo(map).bindPopup(function() {
            var routeList = document.getElementById('route-list');
            var exists = routeList.querySelector(`li[data-id="${attraction.id}"]`);
            var buttonText = exists ? '移出路线' : '加入路线';
            
            return `<h6 class="m-0">${attraction.name}</h6>
                    <p>${attraction.description}</p>
                    <button class="btn btn-sm btn-primary" onclick="toggleRoute('${attraction.id}', '${attraction.name}', this)">${buttonText}</button>`;
        });

        // 存入字典
        attractionMarkers[attraction.id] = marker;

        // 添加点击事件监听
        marker.on('click', function(e) {
            e.originalEvent.stopPropagation();
            selectAttraction(attraction.id);
        });
        marker.on('dragend', function() {
            updateCoord('attractions', attraction.id, this)
        });

        // 添加列表项
        var list = document.getElementById('attraction-list');
        var listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.textContent = attraction.name;
        listItem.setAttribute('data-id', attraction.id); // 设置自定义属性data_id，即景点的id
        listItem.onclick = function() {
            selectAttraction(attraction.id);
        };
        list.appendChild(listItem);
    });
}

function selectAttraction(id) {
    // 如果之前有选中的景点，关闭popup，移除高亮
    if (currentSelected) {
        if (currentSelected.marker) {
            currentSelected.marker.closePopup();
        }
        if (currentSelected.listItem) {
            currentSelected.listItem.classList.remove('active');
        }
    }
    if (id != null){
        var marker, listItem;
        // 选择了入口
        if (id == -1) {
            marker = entranceMarker;
            listItem = null;
        } else {
            marker = attractionMarkers[id];
            listItem = document.querySelector(`li[data-id="${id}"]`);
            listItem.classList.add('active'); // 高亮新的列表项
            listItem.scrollIntoView({behavior: 'smooth', block: 'center'}); // 确保列表项在侧边栏可视区域内
        }
        marker.openPopup();
        // 更新当前选中对象
        currentSelected = { marker: marker, listItem: listItem };
        console.log('当前选中的景点：', marker.options.attractionId, marker.options.attractionName);
    } else {
        currentSelected = null;
        console.log('未选择景点')
    }

    // 如果设施界面active
    if (document.getElementById('amenities-tab').classList.contains('active')) {
        searchAmenity();
    }
    // 如果餐厅界面active
    if (document.getElementById('restaurants-tab').classList.contains('active')) {
        searchRestaurant();
    }

}



function drawRoads() {
    mapData.nodes.forEach(function(node) {
        node.adj.forEach(function(adj) {
            var adjNode_id = adj.id; 
            var adjNode = mapData.nodes[adjNode_id];
            if (adjNode) {
                var color = congestionColors[Math.floor(adj.congestion * 10)];
                var weight = adj.bicycle ? 6 : 3;
                var polyline = L.polyline(
                    [[node.lat, node.lon], [adjNode.lat, adjNode.lon]], 
                    {
                        color: color,
                        weight: weight,
                    }
                ).addTo(map);
                polyline.bindPopup("<div>congestion:" + adj.congestion + "<br>distance:" + adj.distance + "</div>");
            }
        });
    });
}

//------------ 路径规划页面相关函数 -----------
function toggleRoute(id, name, btn) {
    var routeList = document.getElementById('route-list');
    var exists = routeList.querySelector(`li[data-id="${id}"]`);
    var marker = attractionMarkers[id];
    if (!exists) {
        // marker高亮
        marker.setIcon(highlightIcon);
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
        // setActiveTab('routing'); // 切换到路径规划标签
    } else {
        // marker取消高亮
        marker.setIcon(attractionIcon);
        // 如果已在路线中，则移除
        exists.remove();
        btn.textContent = '加入路线';
    }
}
function removeFromRoute(id, listItem) {
    listItem.remove();
    var marker = attractionMarkers[id];
    marker.setIcon(attractionIcon)
    // 更新按钮文本
    var button = document.querySelector(`button[onclick*="toggleRoute('${id}'"]`);
    if (button) {
        button.textContent = '加入路线';
    }
}

// 当点击“规划路径”按钮时触发的函数
function planRoute(mode) {
    // 获取当前加入路线的景点列表
    var allowRide = document.getElementById('allow-ride').checked;
    var routeList = document.getElementById('route-list');
    document.getElementById('planned-routes').classList.add('d-none');
    document.getElementById('cost').classList.add('d-none');
    var loading = document.getElementById('loading');
    loading.classList.remove('d-none');
    var selectedAttractions = [];
    routeList.querySelectorAll('li').forEach(li => {
        selectedAttractions.push(li.getAttribute('data-id'));
    });
    console.log('已选中的景点id序列：', selectedAttractions);
    // 调用后端函数发送请求，并处理返回的 JSON 数据
    fetch('plan_route/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,  // 将 CSRF 令牌包含在请求头中
        },
        body: JSON.stringify({ selected_attractions: selectedAttractions, mode: mode, allow_ride: allowRide }),
    })
    .then(response => response.json())
    .then(data => {
        loading.classList.add('d-none');
        console.log('data: ', data);
        // 在地图上绘制路径
        let latLonSeq = data.latLonSeq;
        console.log('路径规划完成：', latLonSeq);
        displayRoute(latLonSeq);
        displayRouteInfo(mode, data);
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 在侧边栏上展示路径信息的函数
function displayRouteInfo(mode, data) {
    // 侧边栏显示花费时间/路径长度
    var cost = document.getElementById('cost');
    var plannedRoutes = document.getElementById('planned-routes');
    cost.classList.remove('d-none');
    if (data.cost){
        let pre = mode == 'time' ? '最短时间为' : '最短距离为';
        let unit = mode == 'time' ? 's' : 'm';
        cost.innerText = pre + data.cost.toFixed(1) + unit;
    } else {
        cost.innerText = '请至少选择两个景点';
    }
    // 多目标规划展示游览顺序
    if (data.attractionOrder.length != 0) {
        let attrList = document.getElementById('planned-routes-list');
        attrList.innerHTML = '';
        data.attractionOrder.forEach(attrId => {
            let listItem = document.createElement('li');
            listItem.className = 'list-group-item';
            listItem.textContent = attrId == -1 ? '入口' : mapData.attractions[attrId].name;
            listItem.setAttribute('data-id', attrId); // 设置自定义属性data_id，即景点的id
            listItem.onclick = function() {
                selectAttraction(attrId);
            }
            attrList.appendChild(listItem);
        });
        plannedRoutes.classList.remove('d-none');
    } else {
        planRoute.classList.add('d-none');
    }
}


// 在地图上绘制路径的函数
function displayRoute(latLonSeq) {
    routeLayer.clearLayers(); // 清除之前的路径图层
    routeLayer.addLayer(
        L.polyline(latLonSeq, {
        color: 'red',
        weight: 3,
        dashArray: '5,10',
    }))
    console.log("路径绘制完成！");
    
    
}
// -------------设施页面---------------
// 搜索设施并显示
function searchAmenity() {
    // 检查是否有景点被选中
    if (currentSelected && currentSelected.marker) {
        var selectedAttractionId = currentSelected.marker.options.attractionId;
        var searchText = document.getElementById('amenity-search').value; // 获取搜索框中的内容

        // 发起请求，包含当前选中的景点ID和搜索框中的内容
        str = `search_amenity/?id=${selectedAttractionId}&type=${searchText}`
        if (edit) str += '&edit=1';
        fetch(str, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log('设施搜索结果：', data.amenities)
            displayAmenities(data.amenities, data.distances);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } else {
        // 如果没有景点被选中，则显示提示信息
        var amenityList = document.getElementById('amenity-list');
        amenityList.innerHTML = '<li class="list-group-item bg-light text-muted">请选择一个景点</li>';
        amenityLayer.clearLayers();
    }
}


// 显示设施列表和marker标记
function displayAmenities(amenities, distances) {
    // 清空现有设施列表和 marker
    var amenityList = document.getElementById('amenity-list');
    amenityList.innerHTML = '';
    amenityLayer.clearLayers();

    amenities.forEach((amenity, index) => {
        // marker 添加
        var marker = L.marker([amenity.lat, amenity.lon], {
            icon: amenityIcon,
            draggable: edit ? true : false,
            autoPan: edit ? true : false,
        });
        marker.addTo(amenityLayer).bindPopup(
            `<h6 class="m-0">${amenity.name}</h6>
             <p>${amenity.description}</p>`
        );
        // 展示列表
        var listItem = document.createElement('li');
        listItem.setAttribute('data-id', amenity.id);
        listItem.className = 'list-group-item';
        listItem.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <h5>${amenity.name}</h5>
            <span class="text-muted">${distances[index]}m</span>
        </div>
        <span>类别：${amenity.type}</span>`;
        listItem.onclick = function() {
            highlightListItem(listItem, marker);
        }
        amenityList.appendChild(listItem);
        marker.on('click', function (e) {
            e.originalEvent.stopPropagation();
            highlightListItem(listItem, marker);
        });
        marker.on('dragend', function() {
            updateCoord('amenities', amenity.id, this)
        });
    });
}


// -------------美食页面-----------------
// 搜索餐馆并显示
function searchRestaurant() {
    var restaurantList = document.getElementById('restaurant-list');
    // 检查是否有景点被选中
    var selectedAttractionId;
    if (currentSelected && currentSelected.marker) {
        selectedAttractionId = currentSelected.marker.options.attractionId;
        // 移除提示元素
        if (document.getElementById('prompt') != null)
            restaurantList.parentNode.removeChild(document.getElementById('prompt'));
    } else { // 如果没有景点被选中，则显示提示信息，默认距离入口
        selectedAttractionId = 1;
        // 将提示元素插入到restaurantList之前
        if (document.getElementById('prompt') == null){
            // 创建提示元素
            var prompt = document.createElement('p');
            prompt.id = "prompt";
            prompt.className = 'bg-light text-muted ms-2';
            prompt.textContent = '未选择景点，距离默认使用入口计算';
            restaurantList.parentNode.insertBefore(prompt, restaurantList);
    
        }
    }
    var searchType = document.getElementById('food-search-type').value;
    var searchText = document.getElementById('food-search-input').value;
    var sortOption = document.getElementById('restaurant-sort').value;
    var filterOption = document.getElementById('restaurant-filter').value;

    str = `search_restaurant/?id=${selectedAttractionId}&search_type=${searchType}&search=${searchText}&sort=${sortOption}&filter=${filterOption}`
    if (edit) str += '&edit=1';
    // 发起请求，包含当前选中的景点ID和搜索选项
    fetch(str, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        console.log('餐馆搜索结果：', data.restaurants)
        displayRestaurants(data.restaurants, data.distances);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}


// 显示设施列表和marker标记
function displayRestaurants(restaurants, distances) {
    // 清空现有设施列表和 marker
    var restaurantList = document.getElementById('restaurant-list');
    restaurantList.innerHTML = '';
    restaurantLayer.clearLayers();

    restaurants.forEach((restaurant, index) => {
        // marker 添加
        var marker = L.marker([restaurant.lat, restaurant.lon], {
            icon: restaurantIcon,
            draggable: edit ? true : false,
            autoPan: edit ? true : false,
        });
        marker.addTo(restaurantLayer).bindPopup(
            `<h6 class="m-0">${restaurant.name}</h6>
             <p>${restaurant.description}</p>`
        );
        
        // 展示列表
        var listItem = document.createElement('li');
        listItem.className = 'list-group-item';
        listItem.setAttribute('data-id', restaurant.id);
        listItem.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <h5>${restaurant.name}</h5>
                <span class="text-muted">${distances[index]}m</span>
            </div>
            <div">
                <span>⭐${restaurant.rating}</span>
                <span>🔥${restaurant.popularity}</span>
            </div>
            <div>类型：${restaurant.type}</div>
            <div>菜品：${restaurant.foods.join(", ")}</div>`;
        listItem.onclick = function() {
            highlightListItem(listItem, marker);
        }
        restaurantList.appendChild(listItem);
        marker.on('click', function (e) {
            e.originalEvent.stopPropagation();
            highlightListItem(listItem, marker);
        });
        marker.on('dragend', function() {
            updateCoord('restaurants', restaurant.id, this)
        });
    });
}
