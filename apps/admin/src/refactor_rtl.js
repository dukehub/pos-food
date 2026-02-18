
import * as fs from 'fs';
import * as path from 'path';

// Helper function to recursively find files
function findFiles(dir, extensions) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            results = results.concat(findFiles(file, extensions));
        } else {
            if (extensions.some(ext => file.endsWith(ext))) {
                results.push(file);
            }
        }
    });
    return results;
}

const targetDir = '/home/duke/Workspace/pos-food/apps/admin/src';
const files = findFiles(targetDir, ['.vue', '.ts']);

let totalUpdates = 0;

files.forEach(file => {
    let content = fs.readFileSync(file, 'utf8');
    let originalContent = content;

    // Refactor rules
    // Margins
    content = content.replace(/ml-/g, 'ms-');
    content = content.replace(/mr-/g, 'me-');
    content = content.replace(/-ml-/g, '-ms-'); // Negative margins
    content = content.replace(/-mr-/g, '-me-');

    // Paddings
    content = content.replace(/pl-/g, 'ps-');
    content = content.replace(/pr-/g, 'pe-');

    // Borders
    content = content.replace(/border-l-/g, 'border-s-');
    content = content.replace(/border-r-/g, 'border-e-');
    content = content.replace(/border-l /g, 'border-s ');
    content = content.replace(/border-r /g, 'border-e ');

    // Rounded corners
    content = content.replace(/rounded-l-/g, 'rounded-s-');
    content = content.replace(/rounded-r-/g, 'rounded-e-');

    // Text alignment
    content = content.replace(/text-left/g, 'text-start');
    content = content.replace(/text-right/g, 'text-end');

    // Positioning (Be careful with false positives, check context likely needed manually)
    // For now, let's stick to safe utility replacements
    content = content.replace(/left-0/g, 'start-0');
    content = content.replace(/right-0/g, 'end-0');

    if (content !== originalContent) {
        fs.writeFileSync(file, content, 'utf8');
        console.log(`Updated: ${file}`);
        totalUpdates++;
    }
});

console.log(`Total files updated: ${totalUpdates}`);
