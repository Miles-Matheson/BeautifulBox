//
//  HomeViewController.m
//  BeautifulBox
//
//  Created by Miles on 17/2/13.
//  Copyright © 2017年 Miles. All rights reserved.
//

#import "HomeViewController.h"
#import "HomeCell.h"

@interface HomeViewController ()

@end

@implementation HomeViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    
    [self.navigationController setNavigationBarHidden:YES];
    
    UIView *topView = [[UIView alloc]initWithFrame:CGRectMake(0, 0, ScreenWidth, 70)];
    topView.backgroundColor = [UIColor redColor];
    [self.view addSubview:topView];
    
    UIImageView *topImg = [[UIImageView alloc]initWithImage:[UIImage imageNamed:@""]];
    topImg.frame = CGRectMake(10, 10, 100, 30);
    topImg.backgroundColor = [UIColor clearColor];
    topImg.image =[UIImage imageNamed:@""];
    [topView addSubview:topImg];
    
    UILabel*topLab = [[UILabel  alloc]initWithFrame:CGRectMake(0, 0, 0, 0)];
    topLab.backgroundColor= [UIColor grayColor];
    topLab.font = [UIFont systemFontOfSize:11];
    topLab.text = @"从。。。。搜索";
    topLab.alpha = 0.6;
    topLab.textAlignment = NSTextAlignmentCenter;
    topLab.textColor = [UIColor whiteColor];
    [topLab sizeToFit];
    topLab.center = CGPointMake(ScreenWidth/2.,topView.height/2.);
    [topView addSubview:topLab];
    NSLog(@"屏幕宽度是 %.f",ScreenWidth);
    
    UITableView *aTableView = [[UITableView alloc ]initWithFrame:CGRectMake(0, topView.bottom , ScreenWidth,ScreenHeight-topView.height - 49)];
    aTableView.delegate = self;
    aTableView.dataSource = self;
    [self.view addSubview:aTableView];
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}
- (CGFloat)tableView:(UITableView *)tableView heightForRowAtIndexPath:(NSIndexPath *)indexPath
{
    return 30;
    
}
- (NSInteger)tableView:(UITableView *)tableView numberOfRowsInSection:(NSInteger)section
{
    return 10;
    
    
}
- (UITableViewCell *)tableView:(UITableView *)tableView cellForRowAtIndexPath:(NSIndexPath *)indexPath
{
    static NSString *identifier = @"Cell";
    
    HomeCell *cell = [tableView dequeueReusableCellWithIdentifier:identifier];
    
    if (cell == nil) {
        cell = [[HomeCell alloc] initWithStyle:UITableViewCellStyleDefault reuseIdentifier:identifier];
        
        cell.selectionStyle = UITableViewCellSelectionStyleNone;
    }
    cell.titleName = @"张三李四ygkjgykhfdhf";
    cell.imageName = @"";
    //拍照button
    UIButton  *photographButton = [UIButton buttonWithType:UIButtonTypeCustom];
    photographButton.frame = CGRectMake(221 , 10, 100, 44);
    [photographButton setImage:[UIImage imageNamed:@"camera.png"] forState:UIControlStateNormal];
    [photographButton addTarget:self action:@selector(photographButtonClicked:) forControlEvents:UIControlEventTouchUpInside];
    photographButton.tag = indexPath.row;
    [cell.contentView addSubview:photographButton];
    
    return cell;
}

- (void)photographButtonClicked:(UIButton *)button
{
    
}
@end
