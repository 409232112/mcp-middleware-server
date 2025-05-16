$(document).ready(function() {
    let methods = {};
    
    // 打开添加方法弹窗
    $('#addMethodBtn').click(function() {
        $('#methodModal').show();
        $('#methodName, #methodDesc, #apiUrl').val('');
        $('#paramTableBody, #headerTableBody').empty();
    });
    
    // 关闭弹窗
    $('.close, #cancelMethodBtn').click(function() {
        $('#methodModal').hide();
    });
    
    // 添加参数行
    $('#addParamBtn').click(function() {
        const row = `
            <tr>
                <td><input type="text" class="form-control param-name"></td>
                <td><input type="text" class="form-control param-desc"></td>
                <td>
                    <select class="form-control param-type">
                        <option value="string">string</option>
                        <option value="number">number</option>
                        <option value="boolean">boolean</option>
                        <option value="object">object</option>
                    </select>
                </td>
                <td><button class="delete-row">−</button></td>
            </tr>
        `;
        $('#paramTableBody').append(row);
    });
    
    // 添加Header行
    $('#addHeaderBtn').click(function() {
        const row = `
            <tr>
                <td><input type="text" class="form-control header-name"></td>
                <td><input type="text" class="form-control header-value"></td>
                <td><button class="delete-row">−</button></td>
            </tr>
        `;
        $('#headerTableBody').append(row);
    });
    
    // 删除行
    $(document).on('click', '.delete-row', function() {
        $(this).closest('tr').remove();
    });
    
    // 保存方法
    $('#saveMethodBtn').click(function() {
        const methodName = $('#methodName').val().trim();
        const methodDesc = $('#methodDesc').val().trim();
        const apiUrl = $('#apiUrl').val().trim();
        
        if (!methodName || !apiUrl) {
            alert('方法名称和API URL不能为空');
            return;
        }
        
        // 收集参数
        const params = {};
        const requiredParams = [];
        $('#paramTableBody tr').each(function() {
            const paramName = $(this).find('.param-name').val().trim();
            const paramDesc = $(this).find('.param-desc').val().trim();
            const paramType = $(this).find('.param-type').val();
            
            if (paramName) {
                params[paramName] = {
                    type: paramType,
                    description: paramDesc
                };
                requiredParams.push(paramName);
            }
        });
        
        // 收集Headers
        const headers = {};
        $('#headerTableBody tr').each(function() {
            const headerName = $(this).find('.header-name').val().trim();
            const headerValue = $(this).find('.header-value').val().trim();
            
            if (headerName && headerValue) {
                headers[headerName] = headerValue;
            }
        });
        
        // 保存方法
        methods[methodName] = {
            api: apiUrl,
            description: methodDesc,
            parameters: {
                required: requiredParams,
                ...params
            },
            headers: headers
        };
        
        updateApiTable();
        $('#methodModal').hide();
    });
    
    // 更新API表格
    function updateApiTable() {
        $('#apiTableBody').empty();
        
        $.each(methods, function(methodName, method) {
                const row = `
                    <tr>
                        <td>${methodName}</td>
                        <td>${method.description}</td>
                        <td>${method.api}</td>
                        <td class="action-cell">
                            <div class="btn-group btn-group-sm">
                                <button class="btn btn-primary edit-method" data-method="${methodName}">编辑</button>
                                <button class="btn btn-danger delete-method" data-method="${methodName}">删除</button>
                            </div>
                        </td>
                    </tr>
                `;
            $('#apiTableBody').append(row);
        });
        
        // 隐藏JSON输出区域并移除下载按钮
        $('#jsonOutput').hide();
        $('#downloadJson').remove();
    }
    
    // 编辑方法
    $(document).on('click', '.edit-method', function() {
        const methodName = $(this).data('method');
        const method = methods[methodName];
        
        $('#methodName').val(methodName);
        $('#methodDesc').val(method.description);
        $('#apiUrl').val(method.api);
        
        // 清空并填充参数表
        $('#paramTableBody').empty();
        $.each(method.parameters, function(paramName, param) {
            if (paramName !== 'required') {
                const row = `
                    <tr>
                        <td><input type="text" class="form-control param-name" value="${paramName}"></td>
                        <td><input type="text" class="form-control param-desc" value="${param.description}"></td>
                        <td>
                            <select class="form-control param-type">
                                <option value="string" ${param.type === 'string' ? 'selected' : ''}>string</option>
                                <option value="number" ${param.type === 'number' ? 'selected' : ''}>number</option>
                                <option value="boolean" ${param.type === 'boolean' ? 'selected' : ''}>boolean</option>
                                <option value="object" ${param.type === 'object' ? 'selected' : ''}>object</option>
                            </select>
                        </td>
                <td><button class="delete-row">−</button></td>
                    </tr>
                `;
                $('#paramTableBody').append(row);
            }
        });
        
        // 清空并填充Header表
        $('#headerTableBody').empty();
        $.each(method.headers, function(headerName, headerValue) {
            const row = `
                <tr>
                    <td><input type="text" class="form-control header-name" value="${headerName}"></td>
                    <td><input type="text" class="form-control header-value" value="${headerValue}"></td>
                    <td><button class="btn btn-danger delete-row">删除</button></td>
                </tr>
            `;
            $('#headerTableBody').append(row);
        });
        
        // 删除原方法
        delete methods[methodName];
        $('#methodModal').show();
    });
    
    // 删除方法
    $(document).on('click', '.delete-method', function() {
        const methodName = $(this).data('method');
        if (confirm(`确定要删除方法 ${methodName} 吗?`)) {
            delete methods[methodName];
            updateApiTable();
        }
    });
    
    // 生成JSON Schema按钮点击事件
    $('#generateBtn').click(function() {
        if($.isEmptyObject(methods)) {
            alert('请先添加至少一个API方法');
            return;
        }
        const jsonStr = JSON.stringify(methods, null, 2);
        $('#jsonContent').text(jsonStr);
        $('#jsonOutput').show();
        
        // 创建下载和复制按钮
        const blob = new Blob([jsonStr], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const downloadBtn = $('#downloadJson');
        const copyBtn = $('#copyJson');
        
        if(downloadBtn.length === 0) {
            $('.json-schema-container').prepend(`
                <div class="json-buttons">
                    <a id="downloadJson" class="btn btn-success" href="${url}" download="api_schema.json">
                        下载JSON
                    </a>
                    <button id="copyJson" class="btn btn-info ml-2">
                        复制JSON内容
                    </button>
                </div>
            `);
            
            // 添加复制功能
            $('#copyJson').click(function() {
                navigator.clipboard.writeText(jsonStr)
                    .then(() => alert('JSON内容已复制到剪贴板'))
                    .catch(err => alert('复制失败: ' + err));
            });
        } else {
            downloadBtn.attr('href', url);
        }
    });
    
    // 点击外部关闭弹窗
    $(window).click(function(event) {
        if (event.target === $('#methodModal')[0]) {
            $('#methodModal').hide();
        }
    });

    // 导入JSON按钮点击事件
    $('#importJsonBtn').click(function() {
        $('#jsonFileInput').click();
    });

    // 文件选择处理
    $('#jsonFileInput').change(function(e) {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(e) {
            try {
                const jsonData = JSON.parse(e.target.result);
                methods = jsonData;
                updateApiTable();
                // 重置文件输入，允许重复选择同一文件
                $(this).val('');
            } catch (error) {
                alert('JSON解析失败：' + error.message);
            }
        }.bind(this); // 绑定this到文件输入元素
        reader.onerror = function() {
            alert('文件读取失败');
        };
        reader.readAsText(file);
    });
});
