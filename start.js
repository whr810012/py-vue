#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');
const os = require('os');

// 颜色输出
const colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    red: '\x1b[31m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    blue: '\x1b[34m',
    magenta: '\x1b[35m',
    cyan: '\x1b[36m'
};

function colorLog(color, message) {
    console.log(`${colors[color]}${message}${colors.reset}`);
}

function log(message) {
    const timestamp = new Date().toLocaleTimeString();
    console.log(`[${timestamp}] ${message}`);
}

// 检查操作系统
const isWindows = os.platform() === 'win32';
const shell = isWindows ? 'cmd' : 'bash';
const shellFlag = isWindows ? '/c' : '-c';

// 项目路径
const projectRoot = __dirname;
const backendPath = path.join(projectRoot, 'backend');
const frontendPath = path.join(projectRoot, 'frontend');

colorLog('blue', '========================================');
colorLog('blue', '    社区志愿服务系统启动脚本');
colorLog('blue', '========================================');
console.log();

// 存储子进程
let backendProcess = null;
let frontendProcess = null;

// 清理函数
function cleanup() {
    colorLog('yellow', '\n[INFO] 正在停止所有服务...');
    
    if (backendProcess) {
        backendProcess.kill('SIGTERM');
    }
    
    if (frontendProcess) {
        frontendProcess.kill('SIGTERM');
    }
    
    setTimeout(() => {
        colorLog('green', '[SUCCESS] 所有服务已停止');
        process.exit(0);
    }, 2000);
}

// 监听退出信号
process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);
process.on('exit', cleanup);

// 启动后端服务
function startBackend() {
    return new Promise((resolve, reject) => {
        colorLog('yellow', '[INFO] 正在启动后端服务...');
        
        const pythonCmd = isWindows ? 'python' : 'python3';
        backendProcess = spawn(pythonCmd, ['run.py'], {
            cwd: backendPath,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });
        
        backendProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                log(`${colors.magenta}[后端]${colors.reset} ${output}`);
                if (output.includes('Running on')) {
                    resolve();
                }
            }
        });
        
        backendProcess.stderr.on('data', (data) => {
            const output = data.toString().trim();
            if (output && !output.includes('WARNING')) {
                log(`${colors.red}[后端错误]${colors.reset} ${output}`);
            }
        });
        
        backendProcess.on('error', (error) => {
            colorLog('red', `[ERROR] 后端启动失败: ${error.message}`);
            reject(error);
        });
        
        backendProcess.on('exit', (code) => {
            if (code !== 0) {
                colorLog('red', `[ERROR] 后端进程退出，退出码: ${code}`);
            }
        });
        
        // 超时处理
        setTimeout(() => {
            if (backendProcess && !backendProcess.killed) {
                colorLog('green', '[SUCCESS] 后端服务启动完成');
                resolve();
            }
        }, 5000);
    });
}

// 启动前端服务
function startFrontend() {
    return new Promise((resolve, reject) => {
        colorLog('yellow', '[INFO] 正在启动前端服务...');
        
        frontendProcess = spawn('npm', ['run', 'serve'], {
            cwd: frontendPath,
            stdio: ['pipe', 'pipe', 'pipe'],
            shell: true
        });
        
        frontendProcess.stdout.on('data', (data) => {
            const output = data.toString().trim();
            if (output) {
                log(`${colors.cyan}[前端]${colors.reset} ${output}`);
                if (output.includes('App running at')) {
                    resolve();
                }
            }
        });
        
        frontendProcess.stderr.on('data', (data) => {
            const output = data.toString().trim();
            if (output && !output.includes('warning') && !output.includes('deprecated')) {
                log(`${colors.red}[前端错误]${colors.reset} ${output}`);
            }
        });
        
        frontendProcess.on('error', (error) => {
            colorLog('red', `[ERROR] 前端启动失败: ${error.message}`);
            reject(error);
        });
        
        frontendProcess.on('exit', (code) => {
            if (code !== 0) {
                colorLog('red', `[ERROR] 前端进程退出，退出码: ${code}`);
            }
        });
        
        // 超时处理
        setTimeout(() => {
            if (frontendProcess && !frontendProcess.killed) {
                colorLog('green', '[SUCCESS] 前端服务启动完成');
                resolve();
            }
        }, 15000);
    });
}

// 主启动函数
async function start() {
    try {
        // 启动后端
        await startBackend();
        
        // 等待一下再启动前端
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // 启动前端
        await startFrontend();
        
        console.log();
        colorLog('green', '========================================');
        colorLog('green', '    所有服务启动完成！');
        colorLog('green', '========================================');
        console.log();
        console.log('服务地址：');
        colorLog('blue', '  后端API: http://localhost:5000');
        colorLog('blue', '  前端应用: http://localhost:8081');
        console.log();
        colorLog('yellow', '按 Ctrl+C 停止所有服务');
        console.log();
        
        // 保持进程运行
        process.stdin.resume();
        
    } catch (error) {
        colorLog('red', `[ERROR] 启动失败: ${error.message}`);
        cleanup();
    }
}

// 开始启动
start();